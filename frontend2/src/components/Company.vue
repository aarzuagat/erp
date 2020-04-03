<template>
  <div class="container-fluid">
    <div class="row">
      <!-- :update="actualizar" -->

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
            <button class="btn btn-primary" @click="actualizar">Guardar</button>
            <button class="btn btn-warning">Modificar</button>
          </td>
        </tr>
      </table>
    </div>

    <ApolloQuery :query="require('../graphql/companies.gql')">
      <template v-slot="{result: {loading, error, data}}">
        <div v-if="loading">Cargando</div>
        <div v-else-if="error">{{error}}</div>
        <div v-else-if="data">
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
            <tr v-for="(item,index) in data.companies" :key="item.id">
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
                <button class="btn btn-warning">Editar</button>
                <button class="btn btn-danger">Eliminar</button>
              </td>
            </tr>
          </table>
        </div>
        <div></div>
      </template>
    </ApolloQuery>
  </div>
</template>

<script>
// import gql from "graphql-tag";
export default {
  name: "Index",
  async mounted() {},

  data() {
    return {
      listado: [],
      url: `http://127.0.0.1:8000/graphql/`,
      object: {
        id: "",
        fiscalName: "",
        commercialName: "",
        nif: "",
        email: "aweqwef@nauta.cu",
        website: "http://www.sfsdf.cu",
        telephone: "42345234",
        mobile: "45234234",
        address: "sfgsfgsfg ww",
        postalCode: "",
      }
    };
  },
  methods: {
    actualizar() {
      const currentValue = this.object
      this.$apollo.mutate({
        mutation: require("../graphql/AddCompany.gql"),
        variables: {
          input: this.object
        },
        update: (store, { data: { addCompany } }) => {
          const data = store.readQuery({
            query: require("../graphql/companies.gql")
          });
          data.companies.push(addCompany);
          store.writeQuery({
            query: require("../graphql/companies.gql"),
            data
          });
          const todoQuery = {
            query: require("../graphql/companies.gql")
          }
          const todoData = store.readQuery(todoQuery)
          todoData.companies.push(addCompany)
          store.writeQuery({...todoQuery, data:todoData})
        },
        optimisticResponse:{
          __typename:"Mutation",
          addCompany:this.object,
        }
      }).then((data)=>{
            console.log(data)
      }).catch((error)=>{
        console.error(error)
        this.object = currentValue
      });
    }
  }
};
</script>

// mutation{
//   activateCompanies(id:[4,5]){
//     ok
//   }
// }