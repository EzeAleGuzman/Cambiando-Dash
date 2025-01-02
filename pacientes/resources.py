from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import Paciente


class PacienteResource(resources.ModelResource):
    # Definición de campos con sus nombres exactos del CSV
    nombre_completo = fields.Field(attribute="nombre_completo")

    dni = fields.Field(attribute="dni")

    fecha_nacimiento = fields.Field(
        column_name="FECHA NACIMIENTO",
        attribute="fecha_nacimiento",
        widget=DateWidget(format="%d/%m/%Y"),  # Formato de fecha estadounidense
    )

    domicilio = fields.Field(attribute="domicilio")

    localidad = fields.Field(attribute="localidad")

    telefono = fields.Field(attribute="telefono")

    obra_social = fields.Field(attribute="obra_social")

    fecha_ingreso = fields.Field(
        column_name="FECHA INGRESO",
        attribute="fecha_ingreso",
        widget=DateWidget(format="%d/%m/%Y"),
    )

    diagnostico = fields.Field(attribute="diagnostico")

    pases = fields.Field(attribute="pases")

    fecha_pase = fields.Field(
        column_name="FECHA PASE",
        attribute="fecha_pase",
        widget=DateWidget(format="%d/%m/%Y"),
    )

    def before_import_row(self, row, **kwargs):
        # Limpiar DNI de comas y puntos
        if row.get("dni"):
            row["dni"] = row["dni"].replace(",", "").replace(".", "")

        # Convertir guiones o cadenas vacías a None
        for campo in ["domicilio", "localidad", "obra_social"]:
            if row.get(campo) in ["-", '""', ""]:
                row[campo] = None

    class Meta:
        model = Paciente
        import_id_fields = ["dni"]
        fields = (
            "nombre_completo",
            "dni",
            "fecha_nacimiento",
            "domicilio",
            "localidad",
            "telefono",
            "obra_social",
            "fecha_ingreso",
            "diagnostico",
            "pases",
            "fecha_pase",
        )
        skip_unchanged = True
