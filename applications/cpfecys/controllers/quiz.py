@auth.requires_login()
@auth.requires(auth.has_membership('Student') or auth.has_membership('Teacher') or auth.has_membership('Super-Administrator') or auth.has_membership('Academic') or auth.has_membership('Ecys-Administrator'))

def home_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    #project = db(db.project.id==idproject).select().first()  
    return dict(ecys_var = ecys_var, periodo = period, course=project, period=periodo)

def create_quiz():
    #session.attachment_list = []
    #session.attachment_list_temp = []
    #session.attachment_list_temp2 = []
    #session.notification_subject = ''
    #session.notification_message = ''
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    #coursesAdmin = None
    #countcoursesAdmin = db.user_project.id.count()
    #countcoursesAdminT = 0
    #coursesStudent = None
    #countcoursesStudent = db.academic_course_assignation.id.count()
    #coursesStudentT = 0
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    #Obtain the current period of the system and all the register periods
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first()  
    idPregunta = 1;
    return dict(ecys_var = ecys_var, periodo = period, idPregunta = idPregunta, project=project, idperiodoc=idperiodoc, idproject=idproject)

def consult_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    #Obtain the current period of the system and all the register periods
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first()  
    userid = auth.user.id
    cursoid = project.project_id
    cadena = 'uid:'+str(userid)+':curso:'+str(cursoid)+':quiz:*'
    import redis
    r = redis.StrictRedis();
    a = r.keys(cadena);
    return dict(ecys_var = ecys_var, periodo = period, project=project, idperiodoc=idperiodoc, idproject=idproject,a=a)

def consultar_quiz():
    area = db(db.area_level.name=='DTT Tutor Académico').select().first()
    ecys_var=False
    if request.vars['ecys'] == "True":
        ecys_var=True
    import cpfecys
    period = cpfecys.current_year_period()
    idperiodoc = request.vars['period']
    idproject = request.vars['project']
    project = db(db.project.id==idproject).select().first()  
    idPregunta = 1;
    return dict(ecys_var = ecys_var, periodo = period, project=project)

@auth.requires_login()
def aumentarPregunta():
    idQuestion += 1;
    return idQuestion;

@auth.requires_login()
def obtenerQuiz():
    import redis
    r = redis.StrictRedis();
    r.incr("idquiz");
    idq = '{"value":"'+r.get("idquiz")+'"}';
    return idq;

@auth.requires_login()
def GuardarQuiz():
    import redis
    r = redis.StrictRedis();
    ide = request.vars['id']
    preguntas = request.vars['jsonquiz']
    curso = request.vars['project']
    uid = request.vars['uid']
    a = r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"preguntas",preguntas);
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"ejecuciones",0);
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"ganados",0);
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"perdidos",0);
    r.hset("uid:"+uid+":curso:"+curso+":quiz:"+ide,"state",0);

    return a;

def GetQuiz():
    import redis
    r = redis.StrictRedis();
    a = r.get(34);
    return a;

@auth.requires_login()
def take_quiz():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def reportes():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = request.vars['period']
    project = request.vars['project']
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def view_reports():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

@auth.requires_login()
def viewer_quiz():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

def viewer_quiz2():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)

def viewer_quiz3():
    import cpfecys
    period = cpfecys.current_year_period()
    periodo = '3'
    project = '93'
    #project = db(db.project.id==idproject).select().first()  
    return dict(periodo = period, course=project, period=periodo)