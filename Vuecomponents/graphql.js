
export const allCompanies = `query{
                              companies{
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
                                companyconfiguration{
                                  shortName
                                  primaryColor
                                  secondaryColor
                                  logo
                                }
                              }
                            }`

export const allCompanyConfig =  `query{
  configurations{
    id
    shortName
    primaryColor
    secondaryColor
    logo
    company{
      id
      fiscalName
    }
  }
}`