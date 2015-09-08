[![Build Status](https://travis-ci.org/manolo-rocks/manolo_scraper.svg)](https://travis-ci.org/aniversarioperu/manolo_scraper)
[![Coverage Status](https://coveralls.io/repos/manolo-rocks/manolo_scraper/badge.svg?branch=master&service=github)](https://coveralls.io/github/aniversarioperu/manolo_scraper?branch=master)
[![codecov.io](http://codecov.io/github/manolo-rocks/manolo_scraper/coverage.svg?branch=master)](http://codecov.io/github/aniversarioperu/manolo_scraper?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/396d38fe507441fa92d7286d07c8577a/badge.svg)](https://www.quantifiedcode.com/app/project/396d38fe507441fa92d7286d07c8577a)

# All spiders go here
Spiders are based on [Scrapy](https://github.com/scrapy/scrapy).

# Configuration
Create a file `config.json` with the following info:

```javascript
{
    "CRAWLERA_USER": "",
    "CRAWLERA_PASS": "",
    "drivername": "postgres",
    "username": "postgres",
    "host": "localhost",
    "port": "5432",
    "password": "",
    "database": "manolo"
}
```

The database credentials are needed so that the spider will upload data to the
production database.


## List of Entities

* [ ] Ministerio de Transportes y Comunicaciones
    * **url**: http://scrv-reporte.mtc.gob.pe/

* [x] Ministerio de la Mujer
    * **url**: http://webapp.mimp.gob.pe:8080/visitaweb/

* [x] Ministerio de Energia y Minas
    * **url**: http://intranet.minem.gob.pe/GESTION/visitas_pcm/Busqueda/

* [x] Instituto Nacional Penitenciario
    * **url**: http://visitasadm.inpe.gob.pe/VisitasadmInpe/Controller

* [x] Ministerio de Defensa
    * **url**: http://www.mindef.gob.pe/visitas/qryvisitas.php

* [x] Presidencial del Consejo de Ministros
    * **url**: http://hera.pcm.gob.pe/Visitas/controlVisitas/index.php?r=consultas/visitaConsulta/index

* [x] Organismo Supervisor de las Contrataciones del Estado
    * **url**: http://visitas.osce.gob.pe/controlVisitas/index.php?r=consultas/visitaConsulta/index

* [x] Ministerio de Produccion
    * **url**: http://www2.produce.gob.pe/produce/transparencia/visitas/

* [ ] Tribunal Constitucional
    * **url**: http://tc.gob.pe/transparencia/visitas/

* [x] Ministerio de Cultura
    * **url**: http://visitas.mcultura.gob.pe/?r=consultas/visitaConsulta/index

* [x] Ministerio de Justicia
    * **url**: http://app3.minjus.gob.pe:8080/visita_web/consulta_visita_comision

* [ ] Ministerio de Relaciones Exteriores
    * **url**: http://visitas.rree.gob.pe/consultavisitas/

* [ ] Ministerio del Trabajo
    * **url**: http://www.trabajo.gob.pe/visitas.php

* [x] Ministerio de Educacion
    * **url**: http://visitasmed.perueduca.edu.pe/controlVisitas/index.php?r=consultas/visitaConsulta

* [x] Ministerio de Salud
    * **url**: http://intranet5.minsa.gob.pe/RegVisitasCons/listado.aspx

* [x] Ministerio del Ambiente
   * **url**: http://visitas.minam.gob.pe/frmConsulta.aspx

* [x] Ministerio de Agricultura y Riesgo
   * **url**: http://sistemas.minag.gob.pe/visitas/controlVisitas/index.php?r=consultas/visitaConsulta

* [ ] Ministerio de Desarrollo e Inclusion social
    * **url**: http://sdv.midis.gob.pe/sis_visita/Transparencia/Transparencia/TransparenciaVisitas

* [ ] Ministerio de Comercio Exterior y Turismo
    * **url**: http://www.mincetur.gob.pe/visitaspublico/Visitas/FrmVisitantes.aspx

* [x] Congreso de la Republica
   * **url**: http://regvisitas.congreso.gob.pe/regvisitastransparencia/

* [x] Presidencia
    * **url**: http://www.presidencia.gob.pe/visitas/consulta_visitas.php

* [x] Ministerio de Vivienda
    * **url**: http://geo.vivienda.gob.pe/Visitas/controlVisitas/index.php?r=consultas/visitaConsulta/index
