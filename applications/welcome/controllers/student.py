# coding: utf8
# intente algo como
@auth.requires_login()
@auth.requires_membership('Student')
def index():
    assignations = db((db.user_project.assigned_user == auth.user.id)&
                      (db.user_project.assigned_user == db.auth_user.id)&
                      (db.user_project.project == db.project.id)&
                      (db.project.area_level == db.area_level.id)&
                      (db.user_project.period == db.period_year.id)).select()
    cyear_period = get_current_year_period()
    def available_reports(assignation_period):
        import datetime
        current_date = datetime.datetime.now()
        #if it is the first semester then the restriction should be:
        #start date >= January 1 year 00:00:00
        #end date >= January 1 year 00:00:00
        #start date < July 1 year 00:00:00
        #end date < July 1 year 00:00:00
        #if it is the second semester then the restriction should be:
        #start date >= July 1 year 00:00:00
        #end date >= July 1 year 00:00:00
        #start date < Jan 1 year 00:00:00
        #end date < Jan 1 year 00:00:00
        if assignation_period.period == first_period.id:
            date_min = datetime.datetime(assignation_period.yearp, 1, 1)
            date_max = datetime.datetime(assignation_period.yearp, 7, 1)
        else:
            date_min = datetime.datetime(assignation_period.yearp, 7, 1)
            date_max = datetime.datetime(assignation_period.yearp, 1, 1)
        return db((db.report_restriction.start_date <= current_date)&
                  (db.report_restriction.end_date >= current_date)&
                  (db.report_restriction.start_date >= date_min)&
                  (db.report_restriction.end_date >= date_min)&
                  (db.report_restriction.start_date < date_max)&
                  (db.report_restriction.end_date < date_max)&
                  (db.report_restriction.is_enabled == True))

    def available_item_restriction(period_year, user_project):
        return db(((db.item_restriction.period==period_year) |
                    (db.item_restriction.permanent==True))&
                (db.item_restriction.is_enabled==True)&
                (db.item_restriction_area.item_restriction==\
                    db.item_restriction.id)&
                (db.item_restriction_area.area_level==\
                    user_project.project.area_level.id)&
                (db.item_restriction.item_type!=2))

    def restriction_project_exception(item_restriction, assignation):
        return db((db.item_restriction_exception.project== \
                    assignation.project.id)&
                    (db.item_restriction.id==item_restriction))

    def items_instance(item_restriction, assignation):
        return db((db.item.item_restriction==item_restriction.id)&
                    (db.item.assignation==assignation.user_project.id)&
                    (db.item.is_active==True))

    import datetime
    current_date = datetime.datetime.now().date()
    return dict(assignations = assignations,
                available_reports = available_reports,
                current_date = current_date,
                cyear_period = cyear_period,
                available_item_restriction = available_item_restriction,
                items_instance = items_instance,
                restriction_project_exception=restriction_project_exception)

## Validate that the report date restriction and is_enabled restriction apply to current date
def val_rep_restr(report_restriction):
    import datetime
    current_date = datetime.datetime.now()
    rep_restr = db((db.report_restriction.id == report_restriction)&
        (db.report_restriction.start_date <= current_date)&
        (db.report_restriction.end_date >= current_date)&
        (db.report_restriction.is_enabled == True)).select().first()
    return rep_restr != None

## Validate that the report status is editable (it is either 'Draft' or 'Recheck')
def valid_status(report):
    return (report.status == db.report_status(db.report_status.name == 'Draft').id) or \
            (report.status == db.report_status(db.report_status.name == 'Recheck').id)

def get_current_year_period():
    import datetime
    cdate = datetime.datetime.now()
    cyear = cdate.year
    cmonth = cdate.month
    period = second_period
    #current period depends if we are in dates between jan-jun and jul-dec
    if cmonth < 7 :
        period = first_period
    return db.period_year((db.period_year.yearp == cyear)&
                          (db.period_year.period == period))

def val_rep_owner(report):
    usr_rep = db((db.report.id == report)&
            (db.report.assignation == db.user_project.id)&
            (db.user_project.assigned_user == auth.user.id)).select().first()
    return usr_rep != None

@auth.requires_login()
@auth.requires_membership('Student')
def update_data():
    update_data_form = False
    if auth.user != None:
        cuser = db(db.auth_user.id==auth.user.id).select().first()
        form = FORM(
                        DIV(LABEL(T('First Name:')),
                                    INPUT(_name="first_name",
                                        _type="text", _id="first_name",
                                        _value=cuser.first_name,
                                        requires=IS_NOT_EMPTY())),

                        DIV(LABEL(T('Last Name:')),
                                       INPUT(_name="last_name",
                                        _type="text", _id="last_name",
                                         _value=cuser.last_name, 
                                         requires=IS_NOT_EMPTY())),

                        DIV(LABEL(T('Email:')),
                                       INPUT(_name="email",
                                        _type="text", _id="email",
                                        _value=cuser.email,
                                        requires=IS_NOT_EMPTY())),

                        DIV(LABEL(T('Password: (Leave the same for no \
                            change)')),
                                      INPUT(_name="password",
                                        _type="password", _id="password",
                                        _value=cuser.password,
                                        requires=IS_NOT_EMPTY())),

                        DIV(LABEL(T('Repeat password: (Leave the blank for \
                            no change)')),
                                      INPUT(_name="repass",
                                        _type="password", _id="repass")),

                        DIV(LABEL(T('Phone:')),
                                      INPUT(_name="phone", _type="text",
                                        _id="phone", _value=cuser.phone,
                                        requires=IS_LENGTH(minsize=8,
                                                        maxsize=12))),

                        DIV(LABEL(T('Working:')),
                                      INPUT(_name="working",
                                        _type="checkbox", _id="working",
                                        _value=cuser.working)),

                        DIV(LABEL(T('Work Address:')),
                                      INPUT(_name="work_address",
                                        _type="text", _id="work_address",
                                        _value=cuser.work_address)),
                        BR(),
                        DIV(INPUT(_type='submit',
                            _value=T('Update Profile'),
                            _class="btn-primary")),
                            _class="form-horizontal",)
        if form.process().accepted:
            first_name = request.vars['first_name']
            last_name = request.vars['last_name']
            email = request.vars['email']
            password = request.vars['password']
            repass = request.vars['repass']
            phone = request.vars['phone']
            working = request.vars['working']
            work_address = request.vars['work_address']

            #TODO analyze for aditional security steps
            cuser=db(db.auth_user.id==auth.user.id).select().first()
            if cuser != None:
                cuser.first_name = first_name
                cuser.last_name = last_name
                cuser.email = email
                cuser.phone = phone
                cuser.data_updated = True
                if password == repass and len(repass) > 0:
                    #TODO Fix password update
                    cuser.password = db.auth_user.password.validate(password)
                if working:
                    cuser.working = working
                    cuser.work_address = work_address

                cuser.update_record()
                response.flash = 'User data updated!'
                redirect(URL('default', 'index'))
            else:
                response.flash = 'Error!'

        elif form.errors:
            response.flash = 'form has errors'
        else:
            response.flash = 'please fill the form'
    return dict(form=form, update_data_form=True)

@cache.action()
@auth.requires_login()
@auth.requires_membership('Student')
def download():
    item = db(db.item.uploaded_file==request.args[0]).select().first()
    if item != None and item.assignation.assigned_user == auth.user.id:
        return response.download(request, db)
    else:
        session.flash = T('Access Forbidden')
        redirect(URL('default', 'index'))

@auth.requires_login()
@auth.requires_membership('Student')
def item():
    cyear_period = get_current_year_period()
    item_restriction = request.vars['restriction']
    user_project = request.vars['assignation']
    item_query = db((db.item.created==cyear_period)&
                (db.item.item_restriction==item_restriction)&
                (db.item.assignation==user_project))
    item_restriction = db(db.item_restriction.id==\
            item_restriction).select().first()

    if(request.args(0) == 'create'):
        if item_query.select().first() == None:
            if item_restriction.item_type.name == 'File' and \
                item_restriction.teacher_only != True:

                form = FORM(
                            DIV(LABEL(T('Upload '+item_restriction.name+' \
                            File:')),
                            INPUT(_name="upload", 
                                _type="file", _id="first_name", 
                                requires=[IS_NOT_EMPTY(), \
                                            IS_UPLOAD_FILENAME( \
                                            extension='^(pdf|doc|docx)$',\
                                            error_message=T('Invalid Format, \
                                            Please upload only PDF, DOC or \
                                            DOCX files files'))])),
                            BR(),
                            DIV(INPUT(_type='submit',
                                            _value=T('Upload File'),
                                            _class="btn-primary")),
                                            _class="form-horizontal",)
                if form.process().accepted:
                    if request.vars.upload != None:
                        item = db.item.uploaded_file.store( \
                            request.vars.upload.file,  \
                            request.vars.upload.filename)
                        db.item.insert(uploaded_file=item,
                            is_active=True,
                            created=cyear_period,
                            item_restriction=item_restriction.id,
                            assignation=user_project)
                        db.commit()
                        session.flash = T('Item created!')
                        redirect(URL('student', 'index'))
                    else:
                        session.flash = T('Error')
                        redirect(URL('student', 'index'))
                elif form.errors:
                    session.flash = T('Errors')
                    redirect(URL('student', 'index'))
                else:
                    session.flash = T('please fill the form')
                return  dict(form=form, action='create')
        else:
            session.flash = T('Action not allowed')
            redirect(URL('student', 'index'))

    elif(request.args(0) == 'view'):
        item_upload = request.vars['file']
        item = db((db.item.item_restriction==item_restriction)&
            (db.item.assignation==user_project)&
            (db.item.uploaded_file==item_upload)).select().first()
        if item != None and item_restriction.teacher_only != True \
                and item.is_active == True \
                and item.assignation.assigned_user == auth.user.id:
            return dict(item=item, name=item_restriction.name, action='view')
        else:
            session.flash = T('Access Forbidden')
            redirect(URL('student', 'index'))

    elif(request.args(0) == 'edit'):
        item = db((db.item.created==cyear_period)&
            (db.item.item_restriction==item_restriction)&
            (db.item.assignation==user_project)).select().first()
        if item == None or item_restriction.teacher_only == True \
                or item.is_active != True:
            redirect(URL('student', 'index'))
        form = FORM(
                    DIV(LABEL(T('Upload '+item_restriction.name+' \
                        File:')),
                                INPUT(_name="upload", 
                                    _type="file", _id="first_name", 
                                    requires=[IS_NOT_EMPTY(), \
                                            IS_UPLOAD_FILENAME( \
                                            extension='^(pdf|doc|docx)$',\
                                            error_message=T('Invalid Format, \
                                            Please upload only PDF, DOC or \
                                            DOCX files files'))])),
                    BR(),
                    DIV(INPUT(_type='submit', 
                        _value=T('Upload File'), 
                        _class="btn-primary")),
                        _class="form-horizontal",)
        if form.process().accepted:
            if request.vars.upload != None:
                uploaded = db.item.uploaded_file.store(request.vars.upload.file, request.vars.upload.filename)
                item = db((db.item.created==cyear_period)&
                    (db.item.item_restriction==item_restriction)&
                    (db.item.assignation==user_project)).select().first()
                if item != None:
                    item.update_record(uploaded_file = uploaded)
                    db.commit()
                    redirect(URL('student', 'index'))
                elif form.errors:
                    response.flash = "Errors"
                else:
                    response.flash = "please fill the form"
        return  dict(form=form, action='edit')

@auth.requires_login()
@auth.requires_membership('Student')
def report():
    if (request.args(0) == 'create'):
        #get the data & save the report
        assignation = request.vars['assignation']
        report_restriction = request.vars['report_restriction']
        # Validate DB report_restriction to obey TIMING rules
        valid_rep_restr = val_rep_restr(report_restriction)
        # Validate report_restriction
        report_restrict = db.report_restriction(db.report_restriction.id == report_restriction)
        valid_report = report_restrict != None
        # Validate assignation belongs to this user
        assign = db.user_project((db.user_project.id == assignation)&
                                (db.user_project.assigned_user == auth.user.id))
        valid_assignation = assign != None
        # Validate there is not an already inserted report
        valid = db.report((db.report.assignation == assignation)&
                  (db.report.report_restriction == report_restriction)) is None
        if not(assignation and report_restriction and valid and valid_assignation and valid_report
           and valid_rep_restr):
            session.flash = T('Invalid selected assignation and report. Select a valid one.')
            redirect(URL('student','index'))
        import datetime
        current_date = datetime.datetime.now()
        report = db.report.insert(created = current_date,
                             assignation = assignation,
                             report_restriction = report_restriction,
                             status = db.report_status(name = 'Draft'))
        session.flash = T('Report is now a draft.')
        redirect(URL('student','report/edit', vars = dict(report = report.id)))
    elif (request.args(0) == 'edit'):
        ## Get the report id
        report = request.vars['report']
        ## Retrieve report data
        report = db.report(db.report.id == report)
        if not(report):
            session.flash = T('Selected report can\'t be edited. Select a valid report.')
            redirect(URL('student','index'))
        ## Validate report TIMING restriction
        valid_rep_restr = val_rep_restr(report.report_restriction.id)
        if not(valid_rep_restr):
            session.flash = T('Selected report can\'t be edited. Select a valid report.')
            redirect(URL('student','index'))
        ## Validate that the report belongs to user
        valid_report_owner = val_rep_owner(report.id)
        if not(valid_report_owner):
            session.flash = T('Selected report can\'t be edited. Select a valid report.')
            redirect(URL('student','index'))
        ## Validate that the report status is editable (it is either 'Draft' or 'Recheck')
        if not(valid_status(report)):
            session.flash = T('Selected report can\'t be edited. Select a valid report.')
            redirect(URL('student','index'))
        ## Markmin formatting of reports
        LATEX = '<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" align="center"/>'
        markmin_settings = {
            'latex':lambda code: LATEX % code.replace('"','"'),
            'code_cpp':lambda text: CODE(text,language='cpp').xml(),
            'code_java':lambda text: CODE(text,language='java').xml(),
            'code_python':lambda text: CODE(text,language='python').xml(),
            'code_html':lambda text: CODE(text,language='html').xml()}
        return dict(state = 'edit',
                    log_types = db(db.log_type.id > 0).select(),
                    logs = db.log_entry((db.log_entry.report == report.id)).select(),
                    anomalies = db((db.log_type.name == 'Anomaly')&
                                   (db.log_entry.log_type == db.log_type.id)&
                                   (db.log_entry.report == report.id)).count(),
                    markmin_settings = markmin_settings,
                    report = report)
    elif (request.args(0) == 'save'):
        ## get the data & save the report
        report = request.vars['report']
        report = db.report(db.report.id == report)
        ## Validate DB report_restriction to obey TIMING rules
        valid_rep_restr = val_rep_restr(report.report_restriction.id)
        ## Validate that the report status is editable (it is either 'Draft' or 'Recheck')
        if not(valid_status(report)):
            session.flash = T('Selected report can\'t be saved. Select a valid report.')
            redirect(URL('student','index'))
        # Validate assignation belongs to this user
        assign = db.user_project((db.user_project.id == report.assignation)&
                                (db.user_project.assigned_user == auth.user.id))
        valid_assignation = assign != None
        if not(report and valid_assignation and valid_rep_restr):
            session.flash = T('Invalid selected assignation and report. Select a valid one.')
            redirect(URL('student','index'))
        import datetime
        current_date = datetime.datetime.now()
        report.update(created = current_date,
                      status = db.report_status(name = 'Draft'))
        session.flash = T('Draft Updated.')
        redirect(URL('student','index'))
    elif (request.args(0) == 'acceptance'):
        #get the data & save the report
        report = request.vars['report']
        report = db.report(db.report.id == report)
        # Validate DB report_restriction to obey TIMING rules
        valid_rep_restr = val_rep_restr(report.report_restriction.id)
        ## Validate that the report status is editable (it is either 'Draft' or 'Recheck')
        if not(valid_status(report)):
            session.flash = T('Invalid selected assignation and report. Select a valid one.')
            redirect(URL('student','index'))
        # Validate assignation belongs to this user
        assign = db.user_project((db.user_project.id == report.assignation)&
                                (db.user_project.assigned_user == auth.user.id))
        valid_assignation = assign != None
        if not(report and valid_assignation and valid_rep_restr):
            session.flash = T('Invalid selected assignation and report. Select a valid one.')
            redirect(URL('student','index'))
        import datetime
        current_date = datetime.datetime.now()
        report.update_record(created = current_date,
                      status = db.report_status(name = 'Grading'))
        session.flash = T('Report sent to Grading.')
        redirect(URL('student','index'))
    elif (request.args(0) == 'view'):
        #Get the report id
        report = request.vars['report']
        # Validate that the report exists
        report = db.report(db.report.id == report)
        valid = not(report is None)
        # Validate that the report belongs to user
        if valid: valid = val_rep_owner(report.id)
        if valid:
            ## Markmin formatting of reports
            LATEX = '<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" align="center"/>'
            markmin_settings = {
                'latex':lambda code: LATEX % code.replace('"','"'),
                'code_cpp':lambda text: CODE(text,language='cpp').xml(),
                'code_java':lambda text: CODE(text,language='java').xml(),
                'code_python':lambda text: CODE(text,language='python').xml(),
                'code_html':lambda text: CODE(text,language='html').xml()}
            return dict(state='view',
                        log_types = db(db.log_type.id > 0).select(),
                        logs = db((db.log_entry.report == report.id)).select(),
                        anomalies = db((db.log_type.name == 'Anomaly')&
                                   (db.log_entry.log_type == db.log_type.id)&
                                   (db.log_entry.report == report.id)).count(),
                        markmin_settings = markmin_settings,
                        report = report)
        else:
            session.flash = T('Selected report can\'t be viewed. Select a valid report.')
            redirect(URL('student', 'index'))
    else:
        redirect(URL('student', 'index'))
    return dict()

@auth.requires_login()
@auth.requires_membership('Student')
def log():
    if (request.args(0) == 'save'):
        # validate the user owns this report
        report = request.vars['report']
        report = db.report(db.report.id == report)
        valid_report = report != None
        if valid_report: valid_report = val_rep_owner(report.id)
        # validate report is editable
        if valid_report: valid_report = val_rep_restr(report.report_restriction)
        # validate report is 'Draft' or 'Recheck'
        if valid_report: valid_report = valid_status(report)
        # validate we receive log-date, log-type, log-content
        log_type = request.vars['log-type']
        log_date = request.vars['log-date']
        log_content = request.vars['log-content']
        if valid_report: valid_report = (log_type and log_date and log_content)
        if valid_report:
            db.log_entry.insert(log_type = log_type,
                                entry_date = log_date,
                                description = log_content,
                                report = report.id)
            session.flash = T('Log added')
            redirect(URL('student', 'report/edit', vars=dict(report=report.id)))
        else:
            session.flash = T('Operation not allowed.')
            redirect(URL('student', 'index'))
    elif (request.args(0) == 'update'):
        # validate the requested log
        log = request.vars['log']
        log = db.log_entry(db.log_entry.id == log)
        valid_log = log != None
        # validate log report owner is valid
        if valid_log: valid_log = val_rep_owner(log.report)
        # validate report is editable
        if valid_log: valid_log = val_rep_restr(log.report['report_restriction'])
        # validate report is 'Draft' or 'Recheck'
        if valid_log: valid_log = valid_status(db.report(db.report.id == log.report))
        # validate we receive log-date, log-type, log-content
        log_type = request.vars['log-type']
        log_date = request.vars['log-date']
        log_content = request.vars['log-content']
        if valid_log: valid_log = (log_type and log_date and log_content)
        if valid_log:
            log.update_record(log_type = log_type,
                              entry_date = log_date,
                              description = log_content)
            session.flash = T('Log Aupdated')
            redirect(URL('student', 'report/edit', vars=dict(report=log.report)))
        else:
            session.flash = T('Operation not allowed.')
            redirect(URL('student', 'index'))
    elif (request.args(0) == 'delete'):
        # validate the requested log
        log = request.vars['log']
        log = db.log_entry(db.log_entry.id == log)
        valid_log = log != None
        # validate log report owner is valid
        if valid_log: valid_log = val_rep_owner(log.report)
        # validate report is editable
        if valid_log: valid_log = val_rep_restr(log.report['report_restriction'])
        # validate report is 'Draft' or 'Recheck'
        if valid_log: valid_log = valid_status(db.report(db.report.id == log.report))
        if valid_log:
            log.delete_record()
            session.flash = T('Log Deleted')
            redirect(URL('student', 'report/edit', vars=dict(report=log.report)))
        else:
            session.flash = T('Operation not allowed.')
            redirect(URL('student', 'index'))
    return dict()

@auth.requires_login()
@auth.requires_membership('Student')
def project_items():
    import datetime
    cdate = datetime.datetime.now()
    user_project = request.vars['assignation']
    create_current, c_enab_date, creport = False, False, False

    project = db((db.user_project.id==user_project)&
                (db.project.id==db.user_project.project)).select(db.project.ALL).first()

    c_enab_date = db((db.enabled_date.start_date <= cdate)&
             (db.enabled_date.end_date >= cdate)).select().first()

    if c_enab_date:
        creport = db((db.report_head.repor_user==auth.user.id)&
              (db.report_head.enabled_date == c_enab_date.id)&
              (db.report_head.project == project.id)).select(db.report_head.ALL)
        if len(creport) == 0 and c_enab_date:
          create_current = True
          usr_reports = db((db.report_head.repor_user==auth.user.id)&
                 (db.report_head.enabled_date != c_enab_date.id)&
                 (db.report_head.project == project.id)).select()
        else:
          usr_reports = db((db.report_head.repor_user==auth.user.id)&
                 (db.report_head.project == project.id)).select()
    else:
        usr_reports = db((db.report_head.repor_user==auth.user.id)&
                 (db.report_head.project == project.id)).select()
    return locals()
