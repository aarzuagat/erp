<template>
  <div class="container-fluid">
    <form class="bg-secondary text-white">
      <div class="row p-2">
          <div class="col-2">
            Company
            <!-- <input class="form-control" type="text" v-model="object.fiscalName" /> -->
            <select v-model="object.company" class="form-control">
              <option
                v-for="(item,index) in companies"
                :value="item.id"
                :key="index"
              >{{item.commercialName}}</option>
            </select>
          </div>
          <div class="col-2">
            shortName
            <input class="form-control" type="text" v-model="object.shortName" />
          </div>
          <div class="col-2">
            primaryColor
            <input class="form-control" type="color" v-model="object.primaryColor" />
          </div>
          <div class="col-2">
            secondaryColor
            <input class="form-control" type="color" v-model="object.secondaryColor" />
          </div>

          <div class="col-2">
            Logo
            <input class="form-control" type="file" v-on:change="uploadFile" />
          </div>
      </div>
      <div class="row mt-2 ml-3">
          <button v-if="!editando" class="btn btn-primary" @click="guardar">Guardar</button>
          <button v-else class="btn btn-warning ml-2" @click="guardar">Modificar</button>
        </div>
    </form>
    <h1>Listado de configurations</h1>
    <table class="table table-bordered">
      <tr>
        <th>No.</th>

        <td>shortName</td>
        <td>primaryColor</td>
        <td>secondaryColor</td>
        <td>logo</td>
        <td>company</td>
      </tr>
      <tr v-for="(item,index) in listado" :key="item.id">
        <td>{{index+1}}</td>
        <td>{{item.shortName}}</td>
        <td>{{item.primaryColor}}</td>
        <td>{{item.secondaryColor}}</td>
        <td>
          <img :src="item.logo" style="height:10rem" />
        </td>
        <td>{{item.company}}</td>
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
import { allCompanies, allCompanyConfig } from "./graphql";

export default {
  name: "Configuration",
  async mounted() {
    try {
      this.getcompanies();
      this.buscar();
    } catch (error) {
      console.log(error);
    }
  },
  data() {
    return {
      listado: [],
      companies: [],
      object: {
        id: "",
        shortName: "",
        primaryColor: "#ff0000",
        secondaryColor: "#ff0000",
        logo: "",
        company: ""
      },
      url: `http://127.0.0.1:8000/api/`,
      editando:false
    };
  },
  methods: {
    uploadFile() {
      this.object.logo = event.target.files[0];
      console.log(this.object.logo);
    },

    buscar() {
      axios({
        method: "POST",
        url: this.url,
        data: {
          query: allCompanyConfig
        }
      }).then(result => {
        this.listado = result.data.data.configurations;
      });
    },
    guardar() {
      let query = `
                mutation{
                  addConfiguration(id:"${this.object.id}",company:"${this.object.company}",primaryColor:"${this.object.primaryColor}",secondaryColor:"${this.object.secondaryColor}",shortName:"${this.object.shortName}")
                  {
                    companyConfig{
                      id
                      shortName
                      primaryColor
                      secondaryColor
                      logo
                      company{
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
                  }
                }
                `;
      axios.post(this.url, { query: query }).then(response => {
        console.log(response.data);
        let newItem = response.data.data.addConfiguration.companyConfig;
        if (this.object.logo != "") {
          this.storeLogo(this.object.logo, newItem.id);
        }
        this.listado.push(newItem);
        this.clean();
      });
    },
    update() {
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
                                    }
                              )
                  {
                    company{
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
      axios.post(this.url, { query: query }).then(response => {
        this.listado.filter(
          item => response.data.data.addCompany.company.id == item.id
        )[0] = response.data.data.addCompany.company;
      });
    },
    eliminar(id) {
      let query = `
               mutation{
                  deleteCompany(id:${id}){
                    ok
                  }
                }`;
      axios.post(this.url, { query: query }).then(response => {
        console.log(response);
      });
    },
    editar(id) {
      let myObject = this.listado.filter(item => item.id == id);
      this.object = myObject[0];
    },
    getcompanies() {
      axios({
        method: "POST",
        url: this.url,
        data: {
          query: allCompanies
        }
      }).then(result => {
        this.companies = result.data.data.companies.filter(
          x => x.companyconfiguration == null
        );
      });
    },
    storeLogo(logo, id) {
      let formData = new FormData();
      formData.append("file", logo);
      formData.append("id", id);
      axios
        .post("http://127.0.0.1:8000/company-configuration", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => console.info(response))
        .catch(response => console.error(response));
    },
    clean() {
      this.object = {
        id: "",
        shortName: "",
        primaryColor: "",
        secondaryColor: "",
        logo: "",
        company: ""
      };
    }
  }
};
</script>

