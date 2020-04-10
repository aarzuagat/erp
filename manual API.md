# Comencemos

## Comandos útiles
```
python manage.py [comando]
```
Los comandos útile son:

**runserver** correr el servidor  
**createsuperuser** crear superusuario  
**migrate** migrar los cambios de la BD




## Crear consultas (query) en Graphql

Puedes ejecutar la ruta del API y alli tienes a **GraphiQl**, un creador visual de consultas.  
Aclaro que con ctrl+space autocompleta
```
Por ejemplo:
query{
  companies{
    id
    fiscalName
    commercialName
  }
}  
```
Devolverá las columnas id, fiscalName y commercialName de las compañías. Puedes agregar tantos campos como quieras, pero deberían ser solo los que necesites. AH, no importa el formato. En Graphiql tienes algo que se llama PRETTIFY que te formatea para que entiendas mejor.  
En el caso de las relaciones, pues hay que pedirle los campos. Por ejemplo, vamos a coger el color primario de las compañías:  
```
query{
  companies{
    id
    fiscalName
    commercialName
    companyconfiguration{
      primaryColor
    }
  }
}  
```
Aquí puedes agregar todos los campos que desees de companyconfiguration. No está permitido decirle que te devuelva todos los campos de un objeto, debes especificarlo.  
Sugerencia: no escribas la consulta, deja que GraphiQl lo haga por ti.  
### Hacer filtros en consultas
Utilice para ello la ruta del api. Por ejemplo:
```
axios.post('http://127.0.0.1:8000/api/'?nombre=alberto&provincia=1)
axios.post('http://127.0.0.1:8000/api/'?fiscalName=alberto&companyconfiguration__shortName=ete)
```
**1**Esto devolverá las persona que contengan alberto en su nombre y en la provincia 1.  
**2**Esto devolverá los elementos con fiscalName "alberto" y que en su relacion (1-1) companyconfiguration, el shortName contenga ete  
**NOTA** Para acceder a los campos de las relaciones, use este formato: **relacion__atributo** (dos guiones bajos _)



## Operaciones de escritura (Mutations)  

Hay dos tipos de mutaciones, las que llevan como parámetro un input:  
```
mutation{
  addCompany(input:{fiscalName:"ETECSA", commercialName:"Etecsa"(...)}){
    company{
      id
      fiscalName
    }
  }
}
```
Notar que la mutation se llama addMODELO y lleva como parámetro un objeto input con los valores de sus atributos.  
**GraphiQl te ayudará mucho con esto**.  
Luego, no puede faltar la respuesta que deseas del servidor, que es la parte de **company{...}**. Esta es la consulta que quieres de vuelta sobre el objeto que estás insertando.

### Insertar imágenes
Para las imágenes siempre habrá una ruta aparte. Allí debes enviarme un **FormData** con los atributos id y file. En el primero el id del objeto y en el segundo el fichero.
Por defecto se devuelve el objeto.

## Actualizar elementos
Utilice el mismo método que el guardar, recuerda que NO puede faltar el id del elemento dentro de la consulta. Es la forma que tengo de saber que lo que vas es a actualizar y no guardar. Cuando guardas, el id viene así "" .

## Eliminar objetos
Utilice la mutation para correspondiente. Por ejemplo:
```
mutation{
  deleteCompanies(id:[9,10,11]){
    ok
  }
}
```
Eliminará las compañías que tengan los ids dentro del array y devolverá una variable ok booleana con la confirmación de la acción.
**ACLARACIÓN:** En estos casos (relaciones 1-1) se aplica borrado en cascada, por lo que las configuraciones asociadas a esos elementos serán eliminadas.  
Siempre en los eliminar, devolveré un elemento ok binario diciendo si se pudieron eliminar o no.

## Autenticación
**PASO 1**: Para solicitar el token, use la ruta /login/ y envíe los siguientes datos por POST (email, password). De vuelta, tendrá un token válido por 1h.  
**PASO 2**: Para hacer peticiones al API, debe utilizar el header Authorization y pasarle en TOKEN como se muestra
```
Authorization: <token>
```
Si la última petición fue hecha hace más de 1h, recibirá un error 401, por lo que debe volver al **PASO 1**  
El token tiene, por lo tanto, 1h de vida o 30 peticiones. Si supera las 30 peticiones, el token se invalidará y recibirá una respuesta 205 con un nuevo token. Tenga en cuenta que siempre se devolverá un token en el formato y código 205:
```
TOKEN <new Token>
```
**PASO 3**: Para eliminar un token manualmente, utilice la ruta:
```
/delete-token/
```
y envíe por post el campo **token** con el valor. Automáticamente será eliminado y por ende volver al **PASO 1**




