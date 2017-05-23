#cerodas: Manage Catalogs EPS
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def status():
    grid = SQLFORM.grid(db.eps_status)
    return locals()

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def period():
    grid = SQLFORM.grid(db.eps_period)
    return locals()


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def year():
    grid = SQLFORM.grid(db.eps_period_year)
    return locals()


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def modality():
    grid = SQLFORM.grid(db.eps_modality)
    return locals()

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def activity():
    grid = SQLFORM.grid(db.eps_activity)
    return locals()

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def institution():
    grid = SQLFORM.grid(db.eps_institution)
    return locals()

def getNameStudent():
    num_carnet = request.vars.num_carnet;
    if (num_carnet):
        DsStudent = db(db.auth_user.username == num_carnet).select(db.auth_user.ALL).first();
        if (DsStudent):
            return str(DsStudent.first_name) + ' ' + str(DsStudent.last_name) ;
            pass
        else:
            pass
            return '';
    else:
        return '';
    

#cerodas: Functions to Assign Students
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def asign_students():
    #response.flash = request.vars['year_period'];
    #import del modulod
    import cpfecys
    #obtengo el valor pasado como parametro
    year_period = request.vars['year_period']
    #obtengo los ciclos del presente año
    lastperiods = db((db.eps_period_year.yearp == cpfecys.current_year_period().yearp) \
                     & (db.eps_period_year.period == db.eps_period.id)) \
                    .select(db.eps_period_year.id,db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.id)
    #Otros periodos
    other_periods = db((db.eps_period_year.yearp < cpfecys.current_year_period().yearp) \
                     & (db.eps_period_year.period == db.eps_period.id)) \
                    .select(db.eps_period_year.id,db.eps_period_year.yearp, db.eps_period.name, orderby=~db.eps_period_year.id)
    #obtener el ultimo
    if not year_period:
        top1lastperiods = db((db.eps_period_year.yearp == cpfecys.current_year_period().yearp) \
                         & (db.eps_period_year.period == db.eps_period.id)) \
                        .select(db.eps_period_year.id,db.eps_period_year.yearp, db.eps_period.name, orderby=~db.eps_period_year.id, limitby=(0,1)).first()
    else:
        top1lastperiods = db((db.eps_period_year.id == year_period) \
                         & (db.eps_period_year.period == db.eps_period.id)) \
                        .select(db.eps_period_year.id,db.eps_period_year.yearp, db.eps_period.name, orderby=~db.eps_period_year.id, limitby=(0,1)).first()
        pass
    #reemplazar
    #currentyear_period = top1lastperiods.eps_period_year.id
    #current_period_name = T(top1lastperiods.eps_period.name)
    #grid con los resultados del periodo
    grid = SQLFORM.grid(db.eps_assignment.period == top1lastperiods.eps_period_year.id)
    
    return dict(grid = grid,
                top1lastperiods = top1lastperiods,
                lastperiods = lastperiods,
                other_periods = other_periods, test = top1lastperiods)





#cerodas: Functions to appointment activities
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def calendar_activity():
    
    #si traigo valores del request del guardar
    if request.vars.lbl_id:
        #construyo el Query con actividades left calendarizadas
        par_modalidad = request.vars['lbl_modality'][0];
        par_periodo = request.vars['lbl_periodo'][0];
        rows=db((db.eps_activity.modality==par_modalidad)).select(db.eps_activity.ALL, db.eps_activity_calendar.ALL,      left=db(db.eps_activity_calendar.period_year==par_periodo).db.eps_activity_calendar.on(db.eps_activity.id==db.eps_activity_calendar.activity));

        cont=0;
        for row in rows:
            db((db.eps_activity_calendar.activity==str(request.vars.lbl_id[cont])) & (db.eps_activity_calendar.period_year==str(request.vars.lbl_periodo[cont]))).delete();
            cont = cont+1;
            db.commit()
            pass

        cont=0;
        for row in rows:
            db.eps_activity_calendar.insert(activity=request.vars.lbl_id[cont], period_year = par_periodo, date_assign= request.vars.lbl_date_assign[cont])
            cont = cont +1;
            db.commit()
            pass

        response.flash = "Actividades guardadas exitosamente";

    #Obtengo los periodos y modalidades
    periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
    ValuePeriod=[e.eps_period_year.id for e in periods];
    TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];

    #CONSTRUYO EL FORM CON LOS DDL
    form = SQLFORM.factory(
        Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
        Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad."))
)

    if FORM.accepts(form,request.vars, keepvalues=True):
        par_modalidad = request.vars.modality;
        par_periodo = request.vars.period;

        #construyo el Query con actividades left calendarizadas
        rows=db((db.eps_activity.modality==par_modalidad)).select(db.eps_activity.ALL, db.eps_activity_calendar.ALL,      left=db(db.eps_activity_calendar.period_year==par_periodo).db.eps_activity_calendar.on(db.eps_activity.id==db.eps_activity_calendar.activity));

        #ENCABEZADO
        ##consulta de los datos del periodo
        rowsPeriodYear = db((db.eps_period_year.period == db.eps_period.id) & (db.eps_period_year.id==par_periodo)).select(db.eps_period_year.yearp, db.eps_period.name).first();

        ##consulta de los datos de la modalidad
        rowsModality = db(db.eps_modality.id == par_modalidad).select().first();

        #realizo la consulta de las fechas establecidas por periodo y mostrarlas como encabezados
        rowsDateRange = db(db.eps_period_year.id == par_periodo).select(db.eps_period_year.ALL).first();

        DateIni = rowsDateRange.start_date;
        DateFin = rowsDateRange.end_date;

        if rows:
            #tabla
            table = TABLE(
                THEAD(TR( TD(B('ID'), _style='display:none;' ) , TD (B('ORDEN')), TD(B('ACTIVIDAD')), TD(B('FECHA'))
                      )),
                TBODY(
                        [TR(
                            [TD(INPUT(_value=row.eps_activity.id,  _type='text', _name="lbl_id", _id="lbl_id_"+str(row.eps_activity.id)), _id='columna_id_' +str(row.eps_activity.id), _style='display:none;'),
                             TD(INPUT(_value=row.eps_activity.orden, _type='text', _name="lbl_orden", _id="lbl_orden_"+str(row.eps_activity.id), _readonly='True'), _id='columna_orden_'+str(row.eps_activity.id)),
                             TD(INPUT(_value=row.eps_activity.name, _type='text', _name="lbl_name", _id="lbl_name_"+str(row.eps_activity.id), _readonly='True'), _id='columna_actividad_'+str(row.eps_activity.id)),
                             TD( INPUT(_name='lbl_date_assign', _onchange="javascript:checkDate('"+str(DateIni)+"','"+str(DateFin)+"',this.value);", _class='date',_type='date', id_ ='lbl_date_assign_' + str(row.eps_activity.id), _value = row.eps_activity_calendar.date_assign) , _id='columna_fecha_'+str(row.eps_activity.id)),
                             TD(INPUT(_value=par_periodo, _type='text', _name='lbl_periodo', _id="lbl_periodo_" + str(row.eps_activity.id)), _id='columna_periodo_' +str(row.eps_activity.id), _style='display:none;'),
                             TD(INPUT(_value=par_modalidad, _type='text', _name='lbl_modality', _id="lbl_modality_" + str(row.eps_activity.id)), _id='columna_modalidad_' +str(row.eps_activity.id), _style='display:none;')
                             ], _id = 'fila_'+str(row.eps_activity.id)
                        ) for row in rows
                    ]))
            table["_class"] = "table table-striped table-bordered table-condensed"
            
            
            form = FORM(
    XML('<b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'<br>'),
    XML('<b>' + 'Del ' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + ' al ' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b><br><br>' ),
    table,
    INPUT(_type='submit', _value = 'GUARDAR'),
    XML("<a href=" + URL('calendar_activity') + " class='btn' ><i class='icon-arrow-left'></i>REGRESAR</a>"),
    XML("<a href=" + URL('calendar', args=[par_periodo, par_modalidad]) + " class='btn' ><i class='icon-arrow-right'></i>CALENDARIO</a>")
    )
        else:
            form = FORM(
    XML('<b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'<br>'),
    XML('<b>' + 'Del ' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + ' al ' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b><br><br>' ),
    XML("<a href=" + URL('calendar_activity') + " class='btn' ><i class='icon-arrow-left'></i>REGRESAR</a>")
    )
            response.flash = "No existen actividades configuradas para la modalidad seleccionada";

        pass
    pass
    
    return dict(form=form)

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def calendar():
    par_periodo = request.args[0];
    par_modalidad = request.args[1];
    #construyo el Query con actividades
    rows=db((db.eps_activity.modality == par_modalidad)&(db.eps_activity_calendar.period_year==par_periodo)&(db.eps_activity.id==db.eps_activity_calendar.activity)&(db.eps_activity_calendar.date_assign!=None)).select(db.eps_activity.ALL, db.eps_activity_calendar.ALL);
    
    return dict(rows=rows)


@auth.requires_login()
@auth.requires_membership('Academic')
def calendar_student():
    
    #parametro de usuario
    par_student = auth.user.username;
    
    #Verifico las asignaciones del usuario
    assign_eps = db(db.eps_assignment.student == par_student).select(db.eps_assignment.ALL);
    
    if assign_eps:
        #CONSTRUYO EL FORM CON LOS DDL
        form = SQLFORM.factory(Field("Proyect", label="Proyecto de EPS", requires=IS_IN_DB(db(db.eps_assignment.student == par_student), 'eps_assignment.id', 'eps_assignment.project' , zero="Seleccione", error_message = "Seleccione un proyecto.")))

        if FORM.accepts(form,request.vars, keepvalues=True):
            
            #recupero la informacion del proyecto seleccionado
            select_eps = db(db.eps_assignment.id == request.vars.Proyect).select().first();
            
            #obtengo infomracion de la modalidad y del periodo
            ##consulta de los datos del periodo
            rowsPeriodYear = db((db.eps_period_year.period == db.eps_period.id) & (db.eps_period_year.id==select_eps.period)).select(db.eps_period_year.yearp, db.eps_period.name).first();

            ##consulta de los datos de la modalidad
            rowsModality = db(db.eps_modality.id == select_eps.modality).select().first();

            #realizo la consulta de las fechas establecidas por periodo y mostrarlas como encabezados
            rowsDateRange = db(db.eps_period_year.id == select_eps.period).select().first();
            
            #obtengo el conjunto de actividades
            rows=db((db.eps_activity.modality == select_eps.modality)&(db.eps_activity_calendar.period_year==select_eps.period)&(db.eps_activity.id==db.eps_activity_calendar.activity)&(db.eps_activity_calendar.date_assign!=None)).select(db.eps_activity.ALL, db.eps_activity_calendar.ALL);
            
            form1 = FORM(
    XML('<br><center><b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'</center>'),
    XML('<center>' + 'Del <b>' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + '</b> al <b>' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b></center>' ))
            
            
            #DETALLE--------------------------------------------------------------
            #obtengo el listado de Estudiantes asignados 
            DSetAssign = db((db.eps_assignment.modality == select_eps.modality)&(db.eps_assignment.period==select_eps.period)&(db.auth_user.username==db.eps_assignment.student)&(db.eps_assignment.status==db.eps_status.id)&(db.eps_assignment.id == request.vars.Proyect)).select(db.eps_assignment.ALL, db.eps_status.ALL, db.auth_user.ALL, orderby=db.eps_assignment.student);
            
            #obtengo el listado de actividades de la modalidad
            DSetActivity = db(db.eps_activity.modality == select_eps.modality).select(orderby=db.eps_activity.orden);
            
            #si tiene estudiantes asignados
            if DSetAssign:
                #si existen actividades
                if DSetActivity:
                    #Armo la tabla
                    table =  TABLE(
                    THEAD(TR(
                                TD(B('ID_ASSIGNMENT'), _style='display:none;'),
                                TD(B('CARNE'), _style="text-align:center;"),
                                TD (B('NOMBRE'), _style="text-align:center;"),
                                TD(B('ESTADO'), _style="text-align:center;"),
                                [TD( A( B(rowhead.name), _href=URL('eps','activity_details_student', args=[rowhead.id,select_eps.modality,select_eps.period,request.vars.Proyect,0]), _target='_blank' ) , _title=rowhead.description, _style="text-align:center;") for rowhead in DSetActivity]
                          )),
                    TBODY(
                            [TR(
                                [
                                    TD(row.eps_assignment.id, _style='display:none;'),
                                    TD(str(row.eps_assignment.student), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                    TD(str(row.auth_user.first_name) + ' ' + str(row.auth_user.last_name), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                    #TD(str(row.eps_assignment.project)),
                                    TD(str(row.eps_status.name)),
                                    [TD( GetActivityTracking(row.eps_assignment.id, rowhead.id), _readonly="readonly", _style="text-align:center;") for rowhead in DSetActivity]
                                ]
                        ) for row in DSetAssign
                        ]))
                    table["_class"] = "table table-striped table-bordered table-condensed"

                    #Armo el formulario
                    form3 = FORM(
                        XML('<HR>'), 
                        table, 
                        XML('<HR>')
                        )
            
        else:
            rows = form1 = form3 = None;
            
    else:
        form = form1= form3 = None;
        response.flash = "No tiene asignado ningun proyecto de EPS, comuniquese con el Administrador."
        
    return dict(form = form, form1=form1, rows = rows, form3 = form3)


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def activity_details():
    #recupero los valores de parametros
    par_actividad = request.args[0];
    par_modalidad = request.args[1];
    par_periodo = request.args[2];
    
    #Recupero informacion de la actividad y su modalidad y su fecha de Asignacion
    rows = db((db.eps_activity.id==par_actividad)&(db.eps_modality.id==db.eps_activity.modality)&(db.eps_activity_calendar.activity==par_actividad)&(db.eps_activity_calendar.period_year==par_periodo)).select(db.eps_activity.ALL, db.eps_modality.ALL, db.eps_activity_calendar.ALL).first();

    #armo el table
    tableHead = TABLE(
                    TR(
                        TD(LABEL(B('Nombre:')), _style='width:30%;'),
                        TD(LABEL(rows.eps_activity.name), _style='width:70%;')
                        ),
                    TR(
                        TD(LABEL(B('Descripción:')), _style='width:30%;'),
                        TD(LABEL(rows.eps_activity.description), _style='width:70%;')
                        ),
                    TR(
                        TD(LABEL(B('Permite entrega virtual:')), _style='width:30%;'),
                        TD(INPUT(_checked=rows.eps_activity.enable_virtual, _type='checkbox', _readonly='True', _enabled='False'), _style='width:70%;')
                        )
                )
    tableHead["_class"] = "table table-striped table-bordered table-condensed"

    if rows.eps_activity.file1:
        table1 =TABLE( TR(
                    TD(LABEL(B('Archivo 1:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file1)), _style='width:70%;'),
                    )
                )
    else:
        table1 =TABLE( TR(
                TD(LABEL(B('Archivo 1:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table1["_class"] = "table table-striped table-bordered table-condensed"
    
    if rows.eps_activity.file2:
        table2 =TABLE( TR(
                    TD(LABEL(B('Archivo 2:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file2)), _style='width:70%;'),
                    )
                )
    else:
        table2 =TABLE( TR(
                TD(LABEL(B('Archivo 2:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table2["_class"] = "table table-striped table-bordered table-condensed"

    if rows.eps_activity.file3:
        table3 =TABLE( TR(
                    TD(LABEL(B('Archivo 3:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file3)), _style='width:70%;'),
                    )
                )
    else:
        table3 =TABLE( TR(
                TD(LABEL(B('Archivo 3:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table3["_class"] = "table table-striped table-bordered table-condensed"

    #armo el form
    form = FORM(
    XML('<b>Actividad: </b>' + str(rows.eps_activity.name)  + '<br>' ),
    XML('<b>Modalidad: </b>' + str(rows.eps_modality.name)  + '<br>' ),
    XML('<b>Fecha: </b>' + str(rows.eps_activity_calendar.date_assign.strftime('%d-%m-%Y'))  + '<br>' + '<br>'),
    tableHead,    table1,     table2,     table3,
    XML('<br>'),
    XML("<a href=" + URL('calendar', args=[par_periodo, par_modalidad]) + " class='btn' ><i class='icon-arrow-left'></i>REGRESAR</a>"),
    )

    return dict(form=form)



@auth.requires_login()
@auth.requires_membership('Academic')
def activity_details_student():
    #recupero los valores de parametros
    par_actividad = request.args[0];
    par_modalidad = request.args[1];
    par_periodo = request.args[2];
    par_asignacion = request.args[3];
    
    if str(request.args[4])=='1':
        response.flash = 'Actividad Guardada exitosamente';
    
    #Recupero informacion de la actividad y su modalidad y su fecha de Asignacion
    rows = db((db.eps_activity.id==par_actividad)&(db.eps_modality.id==db.eps_activity.modality)&(db.eps_activity_calendar.activity==par_actividad)&(db.eps_activity_calendar.period_year==par_periodo)).select(db.eps_activity.ALL, db.eps_modality.ALL, db.eps_activity_calendar.ALL).first();

    #recupero informacion de la si alguna actividad virtual entregada fue aceptada o rechazada
    rowsTrackinkActivity = db((db.eps_tracking_activity.activity == par_actividad)&(db.eps_tracking_activity.assign==par_asignacion)).select(db.eps_tracking_activity.ALL).first();
    
    #armo el table
    tableHead = TABLE(
                    TR(
                        TD(LABEL(B('Nombre:')), _style='width:30%;'),
                        TD(LABEL(rows.eps_activity.name), _style='width:70%;')
                        ),
                    TR(
                        TD(LABEL(B('Descripción:')), _style='width:30%;'),
                        TD(LABEL(rows.eps_activity.description), _style='width:70%;')
                        )
                )
    tableHead["_class"] = "table table-striped table-bordered table-condensed"

    if rows.eps_activity.file1:
        table1 =TABLE( TR(
                    TD(LABEL(B('Archivo 1:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file1)), _style='width:70%;'),
                    )
                )
    else:
        table1 =TABLE( TR(
                TD(LABEL(B('Archivo 1:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table1["_class"] = "table table-striped table-bordered table-condensed"
    
    if rows.eps_activity.file2:
        table2 =TABLE( TR(
                    TD(LABEL(B('Archivo 2:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file2)), _style='width:70%;'),
                    )
                )
    else:
        table2 =TABLE( TR(
                TD(LABEL(B('Archivo 2:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table2["_class"] = "table table-striped table-bordered table-condensed"

    if rows.eps_activity.file3:
        table3 =TABLE( TR(
                    TD(LABEL(B('Archivo 3:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=rows.eps_activity.file3)), _style='width:70%;'),
                    )
                )
    else:
        table3 =TABLE( TR(
                TD(LABEL(B('Archivo 3:')), _style='width:30%;'),
                TD('', _style='width:70%;'),
                )
                )
    table3["_class"] = "table table-striped table-bordered table-condensed"

    #si la actividad permite entrega virtual
    if str(rows.eps_activity.enable_virtual) == 'True':
        
        #verifico si existe algun archivo previamente cargado
        previus_file = db((db.eps_files_enable_virtual.activity==par_actividad)&(db.eps_files_enable_virtual.assign==par_asignacion)).select().first();
        
        #si la fecha actual es menor o igual que la fecha calendarizada
        if ( datetime.date.today() <= rows.eps_activity_calendar.date_assign):
            if previus_file:
                table4 = TABLE(
                    TR(
                    TD(LABEL(B('Entrega Digital:')), _style='width:30%;'),
                    TD(
                        TABLE(TR(TD(B('Descargar')),TD(
                            A('Descargar', _href=URL('default','download', args=previus_file.files))
                        )),TR(TD(B('Actualizar')),TD(
                            INPUT( _type='file', _class = 'upload', _name = 'fileUpload_activity', _id = 'fileUpload_activity',  requires=IS_NOT_EMPTY() )
                        )))
                    )
                    )
                    )
                table4["_class"] = "table table-striped table-bordered table-condensed"
            else:
                table4 = TABLE(
                    TR(
                    TD(LABEL(B('Entrega Digital:')), _style='width:30%;'),
                    TD(INPUT( _type='file', _class = 'upload', _name = 'fileUpload_activity', _id = 'fileUpload_activity',  requires=IS_NOT_EMPTY() ), _style='width:70%;')
                    )
                    )
                table4["_class"] = "table table-striped table-bordered table-condensed"
        else:
            if previus_file:
                table4 = TABLE(
                    TR(
                    TD(LABEL(B('Entrega Digital:')), _style='width:30%;'),
                    TD(A('Descargar', _href=URL('default','download', args=previus_file.files)), _style='width:70%;'),
                    )
                    )
                table4["_class"] = "table table-striped table-bordered table-condensed"
            else:
                table4 = TABLE(
                    TR(
                    TD(LABEL(B('Entrega Digital:')), _style='width:30%;'),
                    TD(XML('<font color="red">La fecha de entrega digital ha caducado.</font>')), _style='width:70%;'
                    )
                    )
                table4["_class"] = "table table-striped table-bordered table-condensed"
    else:
        table4 = '';
        pass

    if ((rowsTrackinkActivity!=None) & (str(rows.eps_activity.enable_virtual) == 'True')):
        if (str(rowsTrackinkActivity.validated) == 'True'):
            table5 =TABLE( TR(
                        TD(LABEL(B('Calificación:')), _style='width:30%;'),
                        TD(XML('<font color="green">Aprobado</font>'), _style='width:15%;'),
                        TD(rowsTrackinkActivity.observations, _style='width:55%;'), 
                        _style='width:70%;'),
                        )
            pass
        if (str(rowsTrackinkActivity.validated) == 'False'):
            table5 =TABLE( TR(
                        TD(LABEL(B('Calificación:')), _style='width:30%;'),
                        TD(XML('<font color="red">Reprobado</font>'), _style='width:15%;'), 
                        TD(rowsTrackinkActivity.observations, _style='width:55%;'), 
                        _style='width:70%;'),
                        )
            pass
        table5["_class"] = "table table-striped table-bordered table-condensed"
        pass
    if ((rowsTrackinkActivity==None) & (str(rows.eps_activity.enable_virtual) == 'True')):
        table5 =TABLE( TR(
                TD(LABEL(B('Calificación:')), _style='width:30%;'),
                TD(XML('<font color="red">*No ha sido calificado</font>'), _style='width:70%;'),
                )
                )
        table5["_class"] = "table table-striped table-bordered table-condensed"
        pass
    if ((rowsTrackinkActivity==None) & (str(rows.eps_activity.enable_virtual) == 'False')):
        table5 =''
        pass


    if ((str(rows.eps_activity.enable_virtual) == 'True')&( datetime.date.today() <= rows.eps_activity_calendar.date_assign)):
        #armo el form
        form = FORM(
        XML('<b>Actividad: </b>' + str(rows.eps_activity.name)  + '<br>' ),
        XML('<b>Modalidad: </b>' + str(rows.eps_modality.name)  + '<br>' ),
        XML('<b>Fecha: </b>' + str(rows.eps_activity_calendar.date_assign.strftime('%d-%m-%Y'))  + '<br>' + '<br>'),
        tableHead,    table1,     table2,     table3, XML('<HR>'), table4, table5,
        XML('<br>'),
        INPUT(_type='submit', _value = 'GUARDAR'),
        XML("<a href=" + URL('calendar_student') + " class='btn' ><i class='icon-arrow-left'></i>REGRESAR</a>"),
        )
    else:
        #armo el form
        form = FORM(
        XML('<b>Actividad: </b>' + str(rows.eps_activity.name)  + '<br>' ),
        XML('<b>Modalidad: </b>' + str(rows.eps_modality.name)  + '<br>' ),
        XML('<b>Fecha: </b>' + str(rows.eps_activity_calendar.date_assign.strftime('%d-%m-%Y'))  + '<br>' + '<br>'),
        tableHead,    table1,     table2,     table3, XML('<HR>'), table4, table5,
        XML('<br>'),
        XML("<a href=" + URL('calendar_student') + " class='btn' ><i class='icon-arrow-left'></i>REGRESAR</a>"),
        )

    #si le dio Guardar
    if form.accepts(request.vars,formname='form'):
        #obtengo la informacion del archivo a guardar
        archivo = db.eps_files_enable_virtual.files.store(form.vars.fileUpload_activity.file,  form.vars.fileUpload_activity.filename)
        #elimino datos anteriores
        db((db.eps_files_enable_virtual.activity==par_actividad) & (db.eps_files_enable_virtual.assign==par_asignacion)).delete();
        
        #realizo el nuevo insert
        db.eps_files_enable_virtual.insert(activity=par_actividad, assign=par_asignacion, files=archivo);
        redirect(URL(request.application, 'eps', 'activity_details_student', args=[par_actividad, par_modalidad, par_periodo, par_asignacion,1]))
    return dict(form=form)



#cerodas: Make a radioButtonList
#http://www.codedisqus.com/0SxWVXqUPV/how-to-have-an-array-of-radio-buttons-in-post-request-of-web2py.html
def radioArray( name, valuesList, val_request ):
    radios = []
    for v in valuesList:
        if val_request:
            radios.append( INPUT(_type="radio", _name=str(name), _id=str(name), _value=v, value=val_request, _style="margin-left:15%;margin-right:15%;") )
        else:
            radios.append( INPUT(_type="radio", _name=str(name), _id=str(name), _value=v, _style="margin-left:15%;margin-right:15%;") )
        pass
    return radios

#cerodas: Funcion para aprobar actividades digitales
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def tracking_activity():
    rowsActivity = form1 = None;
    #response.flash = request.vars;
    
    #--no existen estudiantes a la modalidad y periodo asignado
    if session['not'] == 1:
        response.flash = "No existen estudiantes asignados a la modalidad seleccionada."
        session['not'] = 0;
        
    #--------------------------INICIO GUARDAR ------------------------------
    if request.vars.lbl_id:
        par_modalidad = request.args[0];
        par_periodo = request.args[1];
        par_actividad = request.args[2];
        
        #join de estudiante asignado a la modalidad y periodo contra actividades virtuales entregadas cuya actividad sea la seleccionada
        rows=db((db.eps_assignment.modality==par_modalidad)&(db.eps_assignment.period==par_periodo)&(db.auth_user.username==db.eps_assignment.student)).select(db.eps_assignment.ALL, db.auth_user.ALL, db.eps_files_enable_virtual.ALL,      left=db(db.eps_files_enable_virtual.activity==par_actividad).db.eps_files_enable_virtual.on((db.eps_files_enable_virtual.assign==db.eps_assignment.id)&(db.eps_files_enable_virtual.activity==par_actividad)));
        
        #elimino lo anterior
        cont=0;
        for row in rows:
            db((db.eps_tracking_activity.activity==par_actividad)&(db.eps_tracking_activity.assign==str(request.vars.lbl_id[cont]))).delete();
            cont = cont+1;
            db.commit()
            pass
        
        #inserto el nuevo
        cont=0;
        for row in rows:
            if request.vars["lbl_validated_" + str(request.vars.lbl_id[cont])]:
                validado = 'False';
                if request.vars["lbl_validated_" + str(request.vars.lbl_id[cont])] == 'True':
                    validado = 'True';
                    pass
                if request.vars["lbl_validated_" + str(request.vars.lbl_id[cont])] == 'False':
                    validado = 'False';
                    pass
                
                db.eps_tracking_activity.insert(activity=par_actividad, assign=request.vars.lbl_id[cont], validated = validado, observations = request.vars.lbl_observation[cont])
                db.commit()
            cont = cont +1;
            pass        
        response.flash = 'Se han guardado las validaciones exitosamente.'
        pass    
    pass
    #---------------------------FIN GUARDAR --------------------------------

    #si estoy mandando argumentos
    passing = request.args;
    if passing:
        par_modalidad = request.args[0];
        par_periodo = request.args[1];
        par_actividad = request.args[2];
        
        #join de estudiante asignado a la modalidad y periodo contra actividades virtuales entregadas cuya actividad sea la seleccionada
        DsetFiles=db((db.eps_assignment.modality==par_modalidad)&(db.eps_assignment.period==par_periodo)&(db.auth_user.username==db.eps_assignment.student)&(db.eps_assignment.status==db.eps_status.id)).select(db.eps_assignment.ALL, db.auth_user.ALL, db.eps_files_enable_virtual.ALL, db.eps_tracking_activity.ALL, db.eps_status.ALL,    left=[db(db.eps_files_enable_virtual.activity==par_actividad).db.eps_files_enable_virtual.on((db.eps_files_enable_virtual.assign==db.eps_assignment.id)&(db.eps_files_enable_virtual.activity==par_actividad)), db.eps_tracking_activity.on((db.eps_assignment.id==db.eps_tracking_activity.assign)&(db.eps_tracking_activity.activity==par_actividad))  ]);

        if DsetFiles:
            #response.flash = DsetFiles;
            #obtengo info de la actividad
            DsetActivity = db(db.eps_activity.id==par_actividad).select().first();

            ##consulta de los datos del periodo
            rowsPeriodYear = db((db.eps_period_year.period == db.eps_period.id) & (db.eps_period_year.id==par_periodo)).select(db.eps_period_year.yearp, db.eps_period.name).first();

            ##consulta de los datos de la modalidad
            rowsModality = db(db.eps_modality.id == par_modalidad).select().first();

            #realizo la consulta de las fechas establecidas por periodo y mostrarlas como encabezados
            rowsDateRange = db(db.eps_period_year.id == par_periodo).select().first();
            
            table =  TABLE(
                THEAD(TR(
                            TD(B('ID_ASSIGNMENT'), _style='display:none;'),
                            TD(B('CARNE'), _style="text-align:center"),
                            TD (B('NOMBRE'), _style="text-align:center"),
                            TD(B('ESTADO'), _style="text-align:center"),
                            TD(B('ARCHIVO'), _style="text-align:center"),
							TD(B('VALIDAR'), _style="text-align:center"),
							TD(B('OBSERVACIONES'), _style="text-align:center")
                      )),
                TBODY(
                        [TR(
                            [
                                TD(INPUT(_value=row.eps_assignment.id,  _type='text', _name="lbl_id", _id="lbl_id"), _style='display:none;'),
                                TD(str(row.eps_assignment.student), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                TD(str(row.auth_user.first_name) + ' ' + str(row.auth_user.last_name), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                TD(str(row.eps_status.name)),
                                TD( A(str(row.eps_files_enable_virtual.files).replace('None','').replace(str(row.eps_files_enable_virtual.files), 'Descargar'), _href=URL('default','download', args=row.eps_files_enable_virtual.files))
                                ),
                                TD(
                                    TABLE( 
                                        THEAD(TR(TD(XML('<font color="green"><B>Aprobar</B></font>')), TD(XML('<font color="red"><B>Reprobar</B></font>')))),
                                        TBODY(
                                        TR(
                                            TD(radioArray("lbl_validated_"+str(row.eps_assignment.id), ['True', 'False'], str(row.eps_tracking_activity.validated).replace('None','')  ), _colspan="2", _style="text-align:center;")
                                        ))
                                    ), _style="text-align:center"
                                ),
                                #TD(INPUT(_type="text", _name="lbl_observation", _id="lbl_observation", _value=str(row.eps_tracking_activity.observations).replace('None','')))
                                TD(TEXTAREA(_name="lbl_observation", _id="lbl_observation", value=str(row.eps_tracking_activity.observations).replace('None',''), _style="Height:60px;"))
                            ]
                    ) for row in DsetFiles]
                ))
            table["_class"] = "table table-striped table-bordered table-condensed"

            form1 = FORM(
            XML('<center><B>' + DsetActivity.name.upper() + '</b></center>'),
            XML('<center><b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'</center>'),
            XML('<center>' + 'Del <b>' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + '</b> al <b>' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b></center>' ),
            table,
            INPUT(_type='submit', _value = 'GUARDAR'),XML("<a href=" + URL('tracking_activity') + " class='btn' ><i></i>CANCELAR</a>"))

            #obtengo las actividades
            virtual = db((db.eps_activity.enable_virtual == 'True')&(db.eps_activity.modality==par_modalidad)).select(db.eps_activity.ALL, orderby='orden');

            if virtual:
                rowsActivity = virtual;
                pass
            else:
                rowsActivity = None;
                response.flash = "No existen actividades configuradas con entrega digital";
            pass
            
            request.vars.modality= par_modalidad;
            request.vars.period = par_periodo;
            
            #Obtengo los periodos y modalidades
            periods = db((db.eps_period_year.period == db.eps_period.id)&(db.eps_period_year.id==par_periodo)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
            ValuePeriod=[e.eps_period_year.id for e in periods];    
            TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];


            #CONSTRUYO EL FORM CON LOS DDL
            form = SQLFORM.factory(
                Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero=None, error_message = "Seleccione un período.")),
                Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality.id==par_modalidad), 'eps_modality.id', 'eps_modality.name', zero=None, error_message = "Seleccione una modalidad."))
                )

        else:
            session['not'] = 1;
            redirect(URL(request.application, 'eps', 'tracking_activity'))
        pass

    else:
        #Obtengo los periodos y modalidades
        periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
        ValuePeriod=[e.eps_period_year.id for e in periods];    
        TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];


        #CONSTRUYO EL FORM CON LOS DDL
        form = SQLFORM.factory(
            Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
            Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad."))
            )

        if FORM.accepts(form,request.vars, keepvalues=True):
            par_modalidad = request.vars.modality;
            par_periodo = request.vars.period;

            #obtengo las actividades
            virtual = db((db.eps_activity.enable_virtual == 'True')&(db.eps_activity.modality==par_modalidad)).select(db.eps_activity.ALL, orderby='orden');

            if virtual:
                rowsActivity = virtual;

                pass
            else:
                rowsActivity = None;
                response.flash = "No existen actividades configuradas con entrega digital";
            pass
        pass
    pass

    return dict(form=form, rowsActivity = rowsActivity, form1=form1)


#funcion en base de asignacion y actividad para verificar si hay actividad digital entregada
def GetActivityTracking(idAssignment, idActivity):
    retorno = []
    
    #conjunto de datos provinientes de actividades seguimiento o entregables
    DsTracking = db((db.eps_tracking.activity==idActivity)&(db.eps_tracking.assign==idAssignment)).select(db.eps_tracking.ALL).first();
    
    #conjunto de datos provinientes de actividades virtuales entregadas registradas
    DsActivityTracking = db((db.eps_tracking_activity.activity == idActivity)&(db.eps_tracking_activity.assign==idAssignment)).select(db.eps_tracking_activity.validated).first();
    
    #Posibles combinaciones-------------------------------------------------------------------------------
    
    #entregado personal y no digital
    if ((DsTracking!=None)&(DsActivityTracking==None)):
        retorno.append( INPUT(_type="checkbox",  _checked="checked", _title="Entrega Personal [Aprobado]", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity)  ) )
    
    #entregado digital y no personal
    if ((DsActivityTracking!=None)&(DsTracking==None)):
        if str(DsActivityTracking.validated)=='True':
            retorno.append( INPUT(_type="checkbox",  _checked="checked", _title="Entrega Digital [Aprobado]", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity)  ) )
        else:
            retorno.append( INPUT(_type="checkbox", _title="Entrega Digital [Reprobado]", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity) ) )
        pass
    
    #entregado digital y entrega personal pero digital aceptado
    if ((DsActivityTracking!=None)&(DsTracking!=None)):
        if str(DsActivityTracking.validated)=='True':
            retorno.append( INPUT(_type="checkbox",  _checked="checked", _title="[Aprobado] por entrega digital, [Aprobado] por validacion de entregable.", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity)  ) )
            pass
        pass
    
    #entregado digital y entrega personal pero digital aceptado
    if ((DsActivityTracking!=None)&(DsTracking!=None)):
        if str(DsActivityTracking.validated)=='False':
            retorno.append( INPUT(_type="checkbox",  _checked="checked", _title="[Reprobado] por entrega digital, [Aprobado] por validacion de entregable.", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity)   ) )
            pass
        pass
    
    #No entregado digital ni presencial
    if ((DsTracking==None)&(DsActivityTracking==None)):
        retorno.append( INPUT(_type="checkbox", _title="No calificado", _id="check_"+str(idAssignment)+"_"+str(idActivity), _name="check_"+str(idAssignment)+"_"+str(idActivity) ) )
        pass


    return retorno



#cerodas: Functions to appointment activities
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def tracking():
    
    #si viene del post de guardar
    if request.vars['lbl_save']:
        #                       0 1 2 3 4 5 6 7 8
        #request de la forma:   c h e c k _ 3 _ 2: 'on'
        #3:idAssignment
        #2:idActivity

        #obtengo el listado de estudiantes asignados
        par_modalidad = request.vars.lbl_par_modalidad;
        par_periodo = request.vars.lbl_par_periodo;

        DSetAssign = db((db.eps_assignment.modality==par_modalidad) & (db.eps_assignment.period==par_periodo)).select(db.eps_assignment.ALL);

        #elimino todos los datos de la tabla tracking para cada asignacion
        for row in DSetAssign:
            db(db.eps_tracking.assign==row.id).delete();
            db.commit()
            pass
        
        
        #inserto los nuevos valores en la tabla tracking para cada asignacion y actividad
        #recorro todos los request buscando los correspondientes al check
        for v in request.vars:
            if (v[:5] == "check"):
                first = v.find('_', 0, len(v));  #5  _
                second = v.find('_', 6, len(v)); #7  _
                par_assign = v[first+1:second];      #   3
                par_activity = v[second+1:len(v)];   #   2

                db.eps_tracking.insert(activity=par_activity, assign=par_assign)
                db.commit()
                pass

        response.flash = 'Entregables guardados satisfactoriamente.';

    #Obtengo los periodos y modalidades
    periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
    ValuePeriod=[e.eps_period_year.id for e in periods];
    
    TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];

    #CONSTRUYO EL FORM CON LOS DDL
    form = SQLFORM.factory(
        Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
        Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad."))
        )

    if FORM.accepts(form,request.vars, keepvalues=True):
        par_modalidad = request.vars.modality;
        par_periodo = request.vars.period;
        
        #ENCABEZADO----------------------------------------------------------
        ##consulta de los datos del periodo
        rowsPeriodYear = db((db.eps_period_year.period == db.eps_period.id) & (db.eps_period_year.id==par_periodo)).select(db.eps_period_year.yearp, db.eps_period.name).first();

        ##consulta de los datos de la modalidad
        rowsModality = db(db.eps_modality.id == par_modalidad).select().first();

        #realizo la consulta de las fechas establecidas por periodo y mostrarlas como encabezados
        rowsDateRange = db(db.eps_period_year.id == par_periodo).select().first();
        
        #DETALLE--------------------------------------------------------------
        #obtengo el listado de Estudiantes asignados 
        DSetAssign = db((db.eps_assignment.modality == par_modalidad)&(db.eps_assignment.period==par_periodo)&(db.auth_user.username==db.eps_assignment.student)&(db.eps_assignment.status==db.eps_status.id)).select(db.eps_assignment.ALL, db.eps_status.ALL, db.auth_user.ALL, orderby=db.eps_assignment.student);
		
        #obtengo el listado de actividades de la modalidad
        DSetActivity = db(db.eps_activity.modality == par_modalidad).select(orderby=db.eps_activity.orden);
        
        #si tiene estudiantes asignados
        if DSetAssign:
            #si existen actividades
            if DSetActivity:
                #Armo la tabla
                table =  TABLE(
                THEAD(TR(
                            TD(B('ID_ASSIGNMENT'), _style='display:none;'),
                            TD(B('CARNE')),
                            TD (B('NOMBRE')),
                            TD(B('ESTADO')),
                            [TD(B(rowhead.name), _title=rowhead.description) for rowhead in DSetActivity]
                      )),
                TBODY(
                        [TR(
                            [
                                TD(row.eps_assignment.id, _style='display:none;'),
                                TD(str(row.eps_assignment.student), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                TD(str(row.auth_user.first_name) + ' ' + str(row.auth_user.last_name), _title='Proyecto: '+ str(row.eps_assignment.project)),
                                #TD(str(row.eps_assignment.project)),
                                TD(str(row.eps_status.name)),
                                [TD( GetActivityTracking(row.eps_assignment.id, rowhead.id), _style="text-align:center") for rowhead in DSetActivity]
                            ]
                    ) for row in DSetAssign
                    ]))
                table["_class"] = "table table-striped table-bordered table-condensed"

                #Armo el formulario
                form = FORM(
                XML('<b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'<br>'),
                XML('<b>' + 'Del ' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + ' al ' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b><br><br>' ), XML('<HR>'),
                table, XML('<HR>'),
                INPUT(_type='submit', _value = 'GUARDAR'),XML("<a href=" + URL('tracking') + " class='btn' ><i></i>CANCELAR</a>"),
                INPUT( _type='text', _value='1', _name="lbl_save", _id="lbl_save", _style='display:none;'),
                INPUT( _type='text', _value=par_modalidad, _name="lbl_par_modalidad", _id="lbl_par_modalidad", _style='display:none;'),
                INPUT( _type='text', _value=par_periodo, _name="lbl_par_periodo", _id="lbl_par_periodo", _style='display:none;')
                )

                #form.element('input[name=lbl_carne]')['_style']='width:80px'
                pass
            else:
                #form = FORM(
                #XML('<b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'<br>'),
                #XML('<b>' + 'Del ' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + ' al ' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b><br><br>' )
                #);
                 #Obtengo los periodos y modalidades
                periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
                ValuePeriod=[e.eps_period_year.id for e in periods];

                TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];

                #CONSTRUYO EL FORM CON LOS DDL
                form = SQLFORM.factory(
                    Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
                    Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad."))
                    );
                response.flash = "No existen actividades configuradas para la modalidad seleccionada.";
                pass
        else:
            #form = FORM(
            #XML('<b>Modalidad: </b>' + rowsModality.name +  ' <b>Período: </b> ' + str(rowsPeriodYear.eps_period.name) + ' - ' + str(rowsPeriodYear.eps_period_year.yearp) +'<br>'),
            #XML('<b>' + 'Del ' + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + ' al ' + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + '</b><br><br>' )
            #);
             #Obtengo los periodos y modalidades
            periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
            ValuePeriod=[e.eps_period_year.id for e in periods];

            TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];

            #CONSTRUYO EL FORM CON LOS DDL
            form = SQLFORM.factory(
                Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
                Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad."))
                ) ;          
            response.flash = "No existen estudiantes asignados para la modalidad y periodo seleccionado.";
            pass
    pass
    
    return dict(form=form)


#para guardar el archivo en la carpeta uploads con el nombre original
#http://stackoverflow.com/questions/8008213/web2py-upload-with-original-filename
import os
import shutil
def store_file(file, filename=None, path=None):
    path = os.path.join(request.folder, "uploads/")
    if not os.path.exists(path):
         os.makedirs(path)
    pathfilename = os.path.join(path, filename)
    dest_file = open(pathfilename, 'wb')
    try:
            shutil.copyfileobj(file, dest_file)
    finally:
            dest_file.close()
    return filename


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def send_email():
    import os

    #Obtengo los periodos y modalidades
    periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
    ValuePeriod=[e.eps_period_year.id for e in periods];

    TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];
    myset = [("1", "")]

    
    ##NUEVO METODO PARA INCLUIR A TODOS EN EL ENVIO DEL CORREO
    Dsmodality = db(db.eps_modality).select(db.eps_modality.ALL);
    ValueModality = [e.id for e in Dsmodality];
    TextModality = [str(e.name)  for e in Dsmodality];
    ValueModality.extend([-1])
    TextModality.extend(['Todos'])
    
    #CONSTRUYO EL FORM CON LOS DDL
    folder = os.path.join(request.folder, "uploads/")
    form = SQLFORM.factory(
            Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
            #Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad.")),
            Field("modality", label="Modalidad", requires=IS_IN_SET(ValueModality, TextModality, zero="Seleccione", error_message = "Seleccione una modalidad.")),
            Field('subject', label="Asunto",  requires=IS_NOT_EMPTY()),
            Field('message', 'string',label="Mensaje", requires=IS_NOT_EMPTY(), widget=SQLFORM.widgets.text.widget),
            Field('attachment',  'upload', label="Adjunto", custom_store=store_file),
            Field('notify',label=B("Copiarme"), type='string', requires=IS_IN_SET(myset, multiple=True), widget=lambda         f,v:SQLFORM.widgets.checkboxes.widget(f,v,style='divs'), default = '0')
        )

    #if FORM.process.accepts(form,request.vars, keepvalues=False):
    if form.process(formname='form').accepted:
        if request.vars:
            #obtengo los valores request
            par_periodo = request.vars.period;
            par_modalidad = request.vars.modality;
            par_subject = request.vars.subject;
            par_message = request.vars.message;
            par_attachment = request.vars.attachment;
            par_notify = request.vars.notify;

            #obtengo el conjunto de estudiantes asignados a la modalidad
            if str(par_modalidad) == str('-1'):
                DsetAssignment = db((db.eps_assignment.period == par_periodo) & (db.eps_assignment.student == db.auth_user.username)).select(db.eps_assignment.ALL, db.auth_user.ALL, orderby=db.auth_user.username);
                pass
            else:
                DsetAssignment = db( (db.eps_assignment.modality == par_modalidad) & (db.eps_assignment.period == par_periodo) & (db.eps_assignment.student == db.auth_user.username)).select(db.eps_assignment.ALL, db.auth_user.ALL, orderby=db.auth_user.username);
                pass

            if DsetAssignment:
                #ENCABEZADO----------------------------------------------------------
                
                #realizo la consulta de las fechas establecidas por periodo y mostrarlas como encabezados
                rowsDateRange = db(db.eps_period_year.id == par_periodo).select().first();
                
                ##consulta de los datos del periodo
                rowsPeriodYear = db((db.eps_period_year.period == db.eps_period.id) & (db.eps_period_year.id==par_periodo)).select(db.eps_period_year.yearp, db.eps_period.name).first();

                if str(par_modalidad) == str('-1'):
                    #armo el footer
                    footer  = "<br><br><HR><br>";
                    footer += "<b>Suscrito a EPS - USAC </b> <br>";
                    footer += "<b>Período: </b> " + str(rowsPeriodYear.eps_period.name) + " - " + str(rowsPeriodYear.eps_period_year.yearp) + "<br>";
                    footer += "<b> Del " + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + " al " + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + "</b><br><br>";
                    footer += "<br><HR><br>";
                    pass
                else:
                    ##consulta de los datos de la modalidad
                    rowsModality = db(db.eps_modality.id == par_modalidad).select().first();

                    #armo el footer
                    footer  = "<br><br><HR><br>";
                    footer += "<b>Suscrito a EPS - USAC </b> <br>";
                    footer += "<b>Modalidad: </b>" + rowsModality.name +  " <b>Período: </b> " + str(rowsPeriodYear.eps_period.name) + " - " + str(rowsPeriodYear.eps_period_year.yearp) + "<br>";
                    footer += "<b> Del " + str(rowsDateRange.start_date.strftime('%d-%m-%Y')) + " al " + str(rowsDateRange.end_date.strftime('%d-%m-%Y')) + "</b><br><br>";
                    footer += "<br><HR><br>";
                    pass


                #INICIO RECORRER --------------------------------
                contador = 0;
                for row in DsetAssignment:
                    if row.auth_user.email:
                        if str(request.vars.attachment):
                            if mail.send(str(row.auth_user.email),str(par_subject),'<html>'+str(par_message)+ footer +'</html>', attachments = mail.Attachment(folder + request.vars.attachment.filename )):
                                contador = contador +1;
                                pass
                        else:
                            if mail.send(str(row.auth_user.email),str(par_subject),'<html>'+str(par_message)+ footer +'</html>'):
                                contador = contador +1;
                                pass
                        pass
                        pass
                    pass
                #FIN RECORRER --------------------------------

                if par_notify:
                    myself = db(db.auth_user.id == auth.user_id).select().first();
                    if myself:
                        if str(request.vars.attachment):
                            mail.send(str(myself.email),str(par_subject),'<html>'+str(par_message) + footer + '</html>', attachments = mail.Attachment(folder + request.vars.attachment.filename))
                        else:
                            mail.send(str(myself.email),str(par_subject),'<html>'+str(par_message) + footer + '</html>')
                        pass
                        pass
                    pass
                
                if contador == 0:
                    response.flash = 'No se ha podido mandar ningun Email, verifique su conexion a internet; si el problema persiste comuniquese con el administrador del sistema.'
                    pass
                if contador == 1:
                    response.flash = 'Email enviado satisfactoriamente a ' + str(contador) + ' estudiante.'
                    pass
                if contador > 1:
                    response.flash = 'Email enviado satisfactoriamente a ' + str(contador) + ' estudiantes.'
                    pass
                
                pass
            else:
                response.flash = 'No existen estudiantes asignados a la Modalidad y Periodo Seleccionado.'
                pass
        pass

    return dict(form=form)


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def assignation_upload():
    
    success = False;
    error_users = [];
    warning_users = [];
    #Obtengo los periodos y modalidades
    periods = db((db.eps_period_year.period == db.eps_period.id)).select(db.eps_period_year.id, db.eps_period_year.yearp, db.eps_period.name, orderby=db.eps_period_year.yearp);
    ValuePeriod=[e.eps_period_year.id for e in periods];
    TextPeriod=[str(e.eps_period_year.yearp)+ ' - ' + str(e.eps_period.name)  for e in periods];
    
    folder = os.path.join(request.folder, "uploads/")
    form = SQLFORM.factory(
        Field("period", label="Período", requires=IS_IN_SET(ValuePeriod, TextPeriod, zero="Seleccione", error_message = "Seleccione un período.")),
        Field("modality", label="Modalidad", requires=IS_IN_DB(db(db.eps_modality), 'eps_modality.id', 'eps_modality.name', zero="Seleccione", error_message = "Seleccione una modalidad.")),
        Field('csvfile',  'upload', label="Archivo (.csv)", requires=IS_UPLOAD_FILENAME(extension='csv', error_message='Debe seleccionar un archivo con extension ".csv" ' ) , custom_store=store_file)
)

    if form.process(formname='form').accepted:
        
        import csv
        success = False
        #Mandatory Info
        par_status = 1;
        par_periodo = request.vars.period;
        par_modalidad = request.vars.modality;


        if request.vars.csvfile != None:
            try:
                folder = os.path.join(request.folder, "uploads/")
                filepathname = str(folder) + str(request.vars.csvfile.filename);
                with open(str(filepathname), 'rb') as csv_file_object:
                    cr = csv.reader(csv_file_object, delimiter=',', quotechar='"')
                    success = True
                    header = next(cr)
                    cont = 0;
                    ok = 0;
                    for row in cr:
                        cont = cont + 1;
                        if row[0]:
                            par_student	= row[0];
                            if row[1]:
                                par_project	= row[1];
                                #---------------
                                #optional Info
                                if row[2]:
                                    par_adviser	= row[2]
                                else:
                                    par_adviser	= '';
                                    row.append("Warning: Fila [" + str(cont) + "]: Estudiante [" + str(par_student) + "]: No tiene informacion de Asesor.")
                                    warning_users.append(row)
                                pass

                                if row[3]:
                                    par_supervisor	= row[3]
                                else:
                                    par_supervisor	= '';
                                    row.append("Warning: Fila [" + str(cont) + "]: Estudiante [" + str(par_student) + "]: No tiene informacion de Supervisor.")
                                    warning_users.append(row)
                                pass

                                if row[4]:
                                    par_institution	= row[4]
                                else:
                                    par_institution	= '';
                                    row.append("Warning: Fila [" + str(cont) + "]: Estudiante [" + str(par_student) + "]: No tiene informacion relacionada de Institucion.")
                                    warning_users.append(row)
                                pass

                                usr = db((db.auth_user.username == str(par_student))&(db.auth_membership.user_id==db.auth_user.id)&(db.auth_membership.group_id==db.auth_group.id)&(db.auth_group.role=='Academic')).select(db.auth_user.ALL).first();

                                if usr:
                                    db.eps_assignment.insert(status= par_status, modality = par_modalidad, period=par_periodo, student = par_student, project = par_project, adviser = par_adviser, supervisor = par_supervisor, institution = par_institution);
                                    ok = ok + 1;
                                else:
                                    row.append(T('Error: ') + T('Estudiante [' + str(par_student) + '] no existe en el sistema o no tiene rol de Estudiante-Academic.'))
                                    error_users.append(row)
                                pass

                            #---------------
                            else:
                                row.append("Error: Fila [" + str(cont) + "]: Estudiante [" +  str(par_student) +"]: Proyecto no especificado")
                                error_users.append(row)
                                pass
                        else:
                            row.append("Error: Fila [" + str(cont) + "]: Estudiante no especificado")
                            error_users.append(row)
                            pass
                    pass
                pass
                if (ok > 0):
                    if (ok==1):
                        response.flash="Se asignó [" + str(ok) + "] estudiante, verifique el resumen del proceso.";
                    if (ok > 1):
                        response.flash="Se asignaron [" + str(ok) + "] estudiantes, verifique el resumen del proceso.";
                    pass
                if (ok == 0):
                    response.flash="No se realizo ninguna asignación de estudiantes, verifique el resumen del proceso.";
                    pass
            except csv.Error:
                response.flash = T('File doesn\'t seem properly encoded.')

    pass
    return dict(success = success, errors = error_users, warnings = warning_users,  form=form)



#REPORTES:  SE UTILIZA AJAX PORQUE HAY UN PROBLEMA CON EL USO DE DOS O MAS SQLFORM.GRID EN LA MISMA VISTA, POR LO QUE SE TIENEN QUE HACER LOADS (CARGAS) DIFERENTES.
def sqlform_grid_all_students():
    queryS = ((db.auth_user.id ==db.auth_membership.user_id) & (db.auth_membership.group_id == 5));
    orderbyS=(db.auth_user.username);
    
    db.auth_user.username.label = 'Carnet';
    db.auth_user.first_name.label = 'Nombres';
    db.auth_user.last_name.label = 'Apellidos';
    
    fieldsS = [db.auth_user.username,
    db.auth_user.first_name,
    db.auth_user.last_name,
    db.auth_user.email,
    db.auth_user.phone,
    db.auth_user.home_address,
    #db.auth_user.photo
    ]

    sqlform_grid_all_students = SQLFORM.grid( query = queryS, fields =fieldsS , orderby = orderbyS, searchable=True, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid3', maxtextlength = 50 );

    return sqlform_grid_all_students


def sqlform_grid_students():
    #ESTUDIANTES
    queryS = db.eps_assignment.student==db.auth_user.username;
    orderbyS=(db.auth_user.username);

    db.auth_user.username.label = 'Carnet';
    db.auth_user.first_name.label = 'Nombres';
    db.auth_user.last_name.label = 'Apellidos';

    fieldsS = [db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        db.auth_user.phone,
        db.auth_user.home_address,
        db.eps_assignment.status,
        db.eps_assignment.modality,
        db.eps_assignment.period,
        db.eps_assignment.project,
        db.eps_assignment.adviser,
        db.eps_assignment.supervisor,
        db.eps_assignment.institution
 ]
    sqlform_grid_students = SQLFORM.grid( query = queryS, fields =fieldsS , orderby = orderbyS, searchable=True, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid1', maxtextlength = 50 );

    return sqlform_grid_students



def sqlform_grid_institutions():
    #INSTITUCIONES
    queryI = db.eps_institution;
    orderbyI=(db.eps_institution.name, db.eps_institution.unit);
    fieldsI = [db.eps_institution.name,
        db.eps_institution.unit,
        db.eps_institution.description,
        db.eps_institution.address,
        db.eps_institution.phone,
        db.eps_institution.email,
        db.eps_institution.owner_name,
        db.eps_institution.owner_phone,
        db.eps_institution.owner_email
        ]
    
    sqlform_grid_institution = SQLFORM.grid(query = queryI, fields =fieldsI , orderby = orderbyI, searchable=True, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid2', maxtextlength = 50 );

    return sqlform_grid_institution


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('EPS-Administrator'))
def reports():
    
    return dict()
