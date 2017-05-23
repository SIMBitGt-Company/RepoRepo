#cerodas: Tesis
@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def status():
    grid = SQLFORM.grid(db.tesis_status, maxtextlength = 75)
    return locals()


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def modality():
    grid = SQLFORM.grid(db.tesis_modality, maxtextlength = 75)
    return locals()



@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def research_areas():
    grid = SQLFORM.grid(db.tesis_research_areas, maxtextlength = 75)
    return locals()



def recursive_child(FILA):
    html = '<b>&emsp;&#164;&emsp;'+ FILA.name.upper() + '</b><br>';
    Ds1 = db(db.tesis_research_areas.parent_research_area == FILA.id).select(db.tesis_research_areas.ALL);
    if (Ds1):
        for l1 in Ds1:
            Ds2 = db(db.tesis_research_areas.parent_research_area == l1.id).select(db.tesis_research_areas.ALL);
            if (Ds2):
                html = html + '<b>&emsp;&emsp;&#187;&emsp;'+ l1.name.upper() + '</b><br>';
                for l2 in Ds2:
                    Ds3 = db(db.tesis_research_areas.parent_research_area == l2.id).select(db.tesis_research_areas.ALL);
                    if (Ds3):
                        html = html + '<b>&emsp;&emsp;&emsp;&#187;&emsp;'+ l2.name.upper() + '</b><br>';
                        for l3 in Ds3:
                            Ds4 = db(db.tesis_research_areas.parent_research_area == l3.id).select(db.tesis_research_areas.ALL);
                            if (Ds4):
                                html = html + '<b>&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l3.name.upper() + '</b><br>';
                                for l4 in Ds4:
                                    Ds5 = db(db.tesis_research_areas.parent_research_area == l4.id).select(db.tesis_research_areas.ALL);
                                    if (Ds5):
                                        html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l4.name.upper() + '</b><br>';
                                        for l5 in Ds5:
                                            Ds6 = db(db.tesis_research_areas.parent_research_area == l5.id).select(db.tesis_research_areas.ALL);
                                            if (Ds6):
                                                html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l5.name.upper() + '</b><br>';
                                                for l6 in Ds6:
                                                    Ds7 = db(db.tesis_research_areas.parent_research_area == l6.id).select(db.tesis_research_areas.ALL);
                                                    if (Ds7):
                                                        html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l6.name.upper() + '</b><br>';
                                                        for l7 in Ds7:
                                                            Ds8 = db(db.tesis_research_areas.parent_research_area == l7.id).select(db.tesis_research_areas.ALL);
                                                            if (Ds8):
                                                                html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l7.name.upper() + '</b><br>';
                                                                for l8 in Ds8:
                                                                    Ds9 = db(db.tesis_research_areas.parent_research_area == l8.id).select(db.tesis_research_areas.ALL);
                                                                    if (Ds9):
                                                                        html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l8.name.upper() + '</b><br>';
                                                                        for l9 in Ds9:
                                                                            Ds10 = db(db.tesis_research_areas.parent_research_area == l9.id).select(db.tesis_research_areas.ALL);
                                                                            if (Ds10):
                                                                                html = html + '<b>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l9.name.upper() + '</b><br>';
                                                                            else:
                                                                                html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l9.name.upper() + '<br>';
                                                                    else:
                                                                        html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l8.name.upper() + '<br>';
                                                            else:
                                                                html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l7.name.upper() + '<br>';
                                                    else:
                                                        html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l6.name.upper() + '<br>';
                                            else:
                                                html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l5.name.upper() + '<br>';
                                    else:
                                        html = html + '&emsp;&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l4.name.upper() + '<br>';
                            else:
                                html = html + '&emsp;&emsp;&emsp;&emsp;&#187;&emsp;'+ l3.name.upper() + '<br>';
                    else:
                        html = html + '&emsp;&emsp;&emsp;&#187;&emsp;'+ l2.name.upper() + '<br>';
            else:
                html = html + '&emsp;&emsp;&#187;&emsp;'+ l1.name.upper() + '<br>';
        pass
    return html;


def makeHTML():
    PrimerNivel = db(db.tesis_research_areas.parent_research_area == None).select(db.tesis_research_areas.ALL);
    if (PrimerNivel):
        html = '';
        for row in PrimerNivel:
            html = html + recursive_child(row) + '</br>'
    else:
        html = '<h3>No existen datos</h3>'

    return html


@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def tutor():
    grid = SQLFORM.grid(db.tesis_tutor)
    return locals()



@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def adviser():
    grid = SQLFORM.grid(db.tesis_adviser)
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

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def asign_topics():
    #busco el id de un estado en proceso
    Dset_ok = db(db.tesis_status.name.upper().like('%PROCESO%')).select(db.tesis_status.id).first();
    if Dset_ok:
        id_ok = str(Dset_ok.id);
    else:
        id_ok = '1';

    #busco el id de un estado que sea vencido
    Dset_vencido = db(db.tesis_status.name.upper().like('%VENCIDO%')).select(db.tesis_status.id).first();
    if Dset_vencido:
        id_vencido = str(Dset_vencido.id);
    else:
        id_vencido = '3';

    #busco todos los estudiantes cuya fecha sea vencida de la actual
    DsStudentOld = db((db.tesis_asigned_topics.topic_date_validity < request.now.date()) & (db.tesis_asigned_topics.status == id_ok)).select();

    #si hay estudiantes en proceso cuya fecha sea vencida automaticamente se actualiza el estado a vencido
    if DsStudentOld:
        for row in DsStudentOld:
            row.update_record(status=id_vencido)
            pass
        pass

    grid = SQLFORM.grid(db.tesis_asigned_topics, maxtextlength = 75, searchable=False, )
    return locals()


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

    sqlform_grid_all_students = SQLFORM.grid( query = queryS, fields =fieldsS , orderby = orderbyS, searchable=True, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid2', maxtextlength = 50 );

    return sqlform_grid_all_students


def sqlform_grid_topics():
    #ESTUDIANTES
    queryS = db.tesis_asigned_topics.student==db.auth_user.username;
    orderbyS=(db.auth_user.username);

    db.auth_user.username.label = 'Carnet';
    db.auth_user.first_name.label = 'Nombres';
    db.auth_user.last_name.label = 'Apellidos';

    fieldsS = [db.auth_user.username,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.email,
        db.auth_user.phone,
        db.tesis_asigned_topics.status,
        db.tesis_asigned_topics.tutor,
        db.tesis_asigned_topics.adviser,
        db.tesis_asigned_topics.topic_name,
        db.tesis_asigned_topics.topic_modality,
        db.tesis_asigned_topics.topic_area,
        db.tesis_asigned_topics.topic_description,
        db.tesis_asigned_topics.topic_protocol,
        db.tesis_asigned_topics.file1,
        db.tesis_asigned_topics.topic_date_approval,
        db.tesis_asigned_topics.topic_date_validity,
        db.tesis_asigned_topics.topic_date_reactivation
 ]
    sqlform_grid_topics = SQLFORM.grid( query = queryS, fields =fieldsS , orderby = orderbyS, searchable=True, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid1', maxtextlength = 100 );

    return sqlform_grid_topics

@auth.requires_login()
@auth.requires(auth.has_membership('Super-Administrator') or auth.has_membership('Tesis-Administrator'))
def reports():
        #busco el id de un estado en proceso
    Dset_ok = db(db.tesis_status.name.upper().like('%PROCESO%')).select(db.tesis_status.id).first();
    if Dset_ok:
        id_ok = str(Dset_ok.id);
    else:
        id_ok = '1';

    #busco el id de un estado que sea vencido
    Dset_vencido = db(db.tesis_status.name.upper().like('%VENCIDO%')).select(db.tesis_status.id).first();
    if Dset_vencido:
        id_vencido = str(Dset_vencido.id);
    else:
        id_vencido = '3';

    #busco todos los estudiantes cuya fecha sea vencida de la actual
    DsStudentOld = db((db.tesis_asigned_topics.topic_date_validity < request.now.date()) & (db.tesis_asigned_topics.status == id_ok)).select();

    #si hay estudiantes en proceso cuya fecha sea vencida automaticamente se actualiza el estado a vencido
    if DsStudentOld:
        for row in DsStudentOld:
            row.update_record(status=id_vencido)
            pass
        pass
    
    
    pass
    return dict()


@auth.requires_login()
@auth.requires_membership('Academic')
def reports_student():

    #response.flash = request.vars;
    obs_default = request.vars.Buscar

    #PARA BUSCAR UN VALOR EN ESPECIFICO
    form = SQLFORM.factory(
                  Field("Buscar", default=obs_default, label=""),
                  formstyle='divs',
                  submit_button="Search",
                  );
    form.add_button('Cancelar', URL('reports_student'));
    
    if form.process().accepted:
        response.flash = "";
        if request.vars.Buscar:
            queryS = (
                        (db.tesis_asigned_topics.tutor==db.tesis_tutor.id)
                        & (db.tesis_asigned_topics.adviser==db.tesis_adviser.id)
                        & (
                            (db.tesis_asigned_topics.topic_name.upper().like('%' + form.vars.Buscar.upper() + '%')) |
                            (db.tesis_asigned_topics.topic_description.upper().like('%' + form.vars.Buscar.upper() + '%')) |

                            (db.tesis_tutor.firstname.upper().like('%' + form.vars.Buscar.upper() + '%')) |
                            (db.tesis_tutor.lastname.upper().like('%' + form.vars.Buscar.upper() + '%')) |
                            (db.tesis_tutor.email.upper().like('%' + form.vars.Buscar.upper() + '%')) |

                            (db.tesis_adviser.firstname.upper().like('%' + form.vars.Buscar.upper() + '%')) |
                            (db.tesis_adviser.lastname.upper().like('%' + form.vars.Buscar.upper() + '%')) |
                            (db.tesis_adviser.email.upper().like('%' + form.vars.Buscar.upper() + '%'))
                          )
                    ) ;
        else:
            queryS = ((db.tesis_asigned_topics.tutor==db.tesis_tutor.id) & (db.tesis_asigned_topics.adviser==db.tesis_adviser.id)) ;
        pass
    else:
        queryS = ((db.tesis_asigned_topics.tutor==db.tesis_tutor.id) & (db.tesis_asigned_topics.adviser==db.tesis_adviser.id)) ;
        pass

    #GRID CON DATOS DE TEMAS DE TESIS
    orderbyS=(db.tesis_asigned_topics.topic_name);

    db.tesis_asigned_topics.topic_name.label = 'Tema de Tesis';
    db.tesis_asigned_topics.topic_description.label = 'Descripción';
    db.tesis_asigned_topics.topic_protocol.label = 'Protocolo';
    db.tesis_tutor.firstname.label = 'Nombres de Asesor';
    db.tesis_tutor.lastname.label = 'Apellidos de Asesor';
    db.tesis_tutor.email.label = 'Email de Asesor';
    db.tesis_adviser.firstname.label = 'Nombres de Tutor';
    db.tesis_adviser.lastname.label = 'Apellidos de Tutor';
    db.tesis_adviser.email.label = 'Email de Tutor';

    fieldsS = [db.tesis_asigned_topics.topic_name,
        db.tesis_asigned_topics.topic_description,
        db.tesis_asigned_topics.topic_protocol,
        db.tesis_adviser.firstname,
        db.tesis_adviser.lastname,
        db.tesis_adviser.email,
        db.tesis_tutor.firstname,
        db.tesis_tutor.lastname,
        db.tesis_tutor.email
         ]
    grid = SQLFORM.grid( query = queryS, fields =fieldsS , orderby = orderbyS, searchable=False, sortable=True, paginate=20, deletable=False, editable=False, create=False, details=False, search_widget='default', _class="web2py_grid", formname='grid1', maxtextlength = 100 );

    return dict(form=form, grid=grid)
