<template>
  <div class="container-fluid">
    <div class="row">
      <table class="table bg-secondary">
        <tr>
          <th>
            Nombre Fiscal
            <input class="form-control" type="text" v-model="object.fiscalName" />
          </th>
          <th>
            Nombre Comercial
            <input class="form-control" type="text" v-model="object.commercialName" />
          </th>
          <th>
            NIF
            <input class="form-control" type="text" v-model="object.nif" />
          </th>
        </tr>
        <tr>
          <th>
            email
            <input class="form-control" type="email" v-model="object.email" />
          </th>
          <th>
            website
            <input class="form-control" type="url" v-model="object.website" />
          </th>
          <th>
            telephone
            <input class="form-control" type="text" v-model="object.telephone" />
          </th>
        </tr>
        <tr>
          <th>
            mobile
            <input class="form-control" type="text" v-model="object.mobile" />
          </th>
          <th>
            address
            <input class="form-control" type="text" v-model="object.address" />
          </th>
          <th>
            postalCode
            <input class="form-control" type="number" v-model="object.postalCode" />
          </th>
        </tr>
        <tr>
          <td colspan="3">
            <button v-if="!editando" class="btn btn-primary" @click="guardar">Guardar</button>
            <button v-else class="btn btn-warning" @click="guardar">Modificar</button>
          </td>
        </tr>
      </table>
    </div>
    <h1>Listado de compañías</h1>
    <table class="table table-bordered">
      <tr>
        <th>No.</th>
        <th>Nombre Fiscal</th>
        <th>Nombre Comercial</th>
        <th>NIF</th>
        <td>email</td>
        <td>website</td>
        <td>telephone</td>
        <td>mobile</td>
        <td>address</td>
        <td>postalCode</td>
        <td>Actions</td>
      </tr>
      <tr v-for="(item,index) in listado" :key="item.id">
        <td>{{index+1}}</td>
        <td>{{item.fiscalName}}</td>
        <td>{{item.commercialName}}</td>
        <td>{{item.nif}}</td>
        <td>{{item.email}}</td>
        <td>{{item.website}}</td>
        <td>{{item.telephone}}</td>
        <td>{{item.mobile}}</td>
        <td>{{item.address}}</td>
        <td>{{item.postalCode}}</td>
        <td>
          <button class="btn btn-warning" @click="editar(item.id)">Editar</button>
          <button class="btn btn-danger" @click="eliminar(item.id)">Eliminar</button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { allCompanies } from "./graphql";
export default {
  name: "Index",
  async mounted() {
    try {
      this.buscar();
    } catch (error) {
      console.log(error);
    }
  },
  data() {
    return {
      listado: [],
      object: {
        id: "",
        fiscalName: "",
        commercialName: "",
        nif: "",
        email: "user@dfsdf.com",
        website: "http://test.test.cu",
        telephone: "23453",
        mobile: "3434",
        address: "fsf dfgsdfgsf sdf",
        postalCode: "343",
        configuration: ""
      },
      url: `http://127.0.0.1:8000/api/`,
      editando: false
    };
  },
  methods: {
    buscar() {
      axios({
        method: "POST",
        url: `${this.url}`,
        data: {
          query: allCompanies
        }
      }).then(result => {
        this.listado = result.data.data.companies;
      });
    },
    guardar() {
      let query = `
                mutation{
                    addCompany(input:{
                                      id:"${this.object.id}",
                                      fiscalName:"${this.object.fiscalName}",
                                      commercialName:"${this.object.commercialName}",
                                      nif:"${this.object.nif}",
                                      email:"${this.object.email}",
                                      website:"${this.object.website}",
                                      telephone:"${this.object.telephone}",
                                      mobile:"${this.object.mobile}",
                                      address:"${this.object.address}",
                                      postalCode:"${this.object.postalCode}",
                                      isActive:1,
                                    }
                              )
                  {
                    company{
                      id
                      fiscalName
                      commercialName
                      nif
                      email
                      website
                      telephone
                      mobile
                      address
                      postalCode
                    }
                  }
                }`;
                console.log(query)
      axios.post(this.url, { query: query }).then(response => {
        const item = response.data.data.addCompany.company;
        if (!this.editando) {
          this.listado.push(item);
        } else {
          const oldItems = this.listado.filter(x => x.id != item.id);
          this.listado = [item, ...oldItems];
        }
        this.editando = false;
        this.clean();
      });
    },
    eliminar(id) {
      let query = `
               mutation{
                  deleteCompany(id:${id}){
                    ok
                  }
                }`;
      axios.post(this.url, { query: query }).then(() => {
        this.listado = this.listado.filter(item => item.id != id);
      });
    },
    editar(id) {
      let myObject = this.listado.filter(item => item.id == id);
      this.object = myObject[0];
      this.editando = true;
    },
    clean() {
      this.object = {
        id: "",
        fiscalName: "",
        commercialName: "",
        nif: "",
        email: "",
        website: "",
        telephone: "",
        mobile: "",
        address: "",
        postalCode: "",
        configuration: ""
      };
    }
  }
};
</script>

// mutation{
//   activateCompanies(id:[4,5]){
//     ok
//   }
// }