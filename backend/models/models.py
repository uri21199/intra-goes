from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personal(db.Model):
    __tablename__ = 'personal'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    area = db.Column(db.Enum('Tecnico', 'Sistemas', 'Ambiental', 'Gerencia'), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo'), default='activo')

class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    permisos = db.relationship('RolesPermisos', backref='rol', lazy=True)

class Permisos(db.Model):
    __tablename__ = 'permisos'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)

class RolesPermisos(db.Model):
    __tablename__ = 'roles_permisos'

    id_rol = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    id_permiso = db.Column(db.Integer, db.ForeignKey('permisos.id'), primary_key=True)

class Tickets(db.Model):
    __tablename__ = 'tickets'

    id_ticket = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.Enum('baja', 'media', 'alta'), default='media')
    estado = db.Column(db.Enum('pendiente', 'en progreso', 'completado'), default='pendiente')
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_limite = db.Column(db.DateTime)
    id_asignado = db.Column(db.Integer, db.ForeignKey('personal.id'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias_tickets.id_categoria'))
    ultima_actualizacion = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    usuario_etiquetado = db.Column(db.Integer, db.ForeignKey('personal.id'))
    seguimientos = db.relationship('SeguimientoTickets', backref='ticket', lazy=True)

class Clientes(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto_principal = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(255))
    tickets = db.relationship('Tickets', backref='cliente', lazy=True)

class SeguimientoTickets(db.Model):
    __tablename__ = 'seguimiento_tickets'

    id_seguimiento = db.Column(db.Integer, primary_key=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id_ticket'), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Enum('pendiente', 'en progreso', 'completado'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('personal.id'))

class TicketsAsignaciones(db.Model):
    __tablename__ = 'tickets_asignaciones'

    id_asignacion = db.Column(db.Integer, primary_key=True)
    id_ticket = db.Column(db.Integer, db.ForeignKey('tickets.id_ticket'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    rol = db.Column(db.Enum('creador', 'responsable', 'colaborador'), default='colaborador')
    fecha_asignacion = db.Column(db.DateTime, default=db.func.current_timestamp())

class Ausencias(db.Model):
    __tablename__ = 'ausencias'

    id_ausencia = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    tipo = db.Column(db.Enum('vacaciones', 'médico', 'estudio'), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'aprobado', 'rechazado'), default='pendiente')

class DisponibilidadAcademica(db.Model):
    __tablename__ = 'disponibilidad_academica'

    id_disponibilidad = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    materia = db.Column(db.String(100), nullable=False)
    dias = db.Column(db.String(100), nullable=False)
    horarios = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'aprobado', 'rechazado'), default='pendiente')
    id_aprobador = db.Column(db.Integer, db.ForeignKey('personal.id'))
    fecha_solicitud = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_resolucion = db.Column(db.DateTime)

class Notificaciones(db.Model):
    __tablename__ = 'notificaciones'

    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_destinatario = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.Enum('general', 'ticket', 'aprobacion_dia', 'aprobacion_disponibilidad'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.Enum('leído', 'no leído'), default='no leído')
    id_relacionado = db.Column(db.Integer)


class CategoriasTickets(db.Model):
    __tablename__ = 'categorias_tickets'

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    tickets = db.relationship('Tickets', backref='categoria', lazy=True)

class ConfiguracionGeneral(db.Model):
    __tablename__ = 'configuracion_general'

    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(255), nullable=False)

class NotificacionesGenerales(db.Model):
    __tablename__ = 'notificaciones_generales'

    id_notificacion = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(db.DateTime, default=db.func.current_timestamp())
    fecha_vigencia = db.Column(db.DateTime)
    id_creador = db.Column(db.Integer, db.ForeignKey('personal.id'), nullable=False)
    visible_para = db.Column(db.Enum('todos', 'jefes', 'operadores'), default='todos')
