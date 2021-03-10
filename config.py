run_selenium = True

options_ids = {
    "otras": 336,  # Nacimiento y cuidado de menor, con o sin asistencia sanitaria, incapacidad temporal, prestaciones familiares, riesgos embarazo y lactancia
    "pensiones": 335,  # Pensiones de jubilacion, incapacidad permanente, viudedad, orfandad y favor de familiares
    "telefonica": 343,  # Con este servicio se llamará telefónicamente al ciudadano a la hora elegida en la cita. NO ACUDIR A LA OFICINA
    "cert_digital": 342,  # Solicitud de certificado digital o certificado Cl@ve Permanente
    "ingreso_minimo_vital": 341  # Nueva prestación de ingreso mínimo vital
}

options_ids_interface_map = {
    "Pensiones": "pensiones",
    "Cita Telefónica (no se acude a la oficina)": "telefonica",
    "Certificado Digital": "cert_digital",
    "Ingreso Mínimo Vital": "ingreso_minimo_vital",
    "Otro": "otras"
}

options_ids_interface_order = [
    "Pensiones",
    "Certificado Digital",
    "Ingreso Mínimo Vital",
    "Cita Telefónica (no se acude a la oficina)",
    "Otro"
]

if set(options_ids_interface_map.keys()) != set(options_ids_interface_order):
    raise Exception("Every interface option in ordered list should have a mapping")