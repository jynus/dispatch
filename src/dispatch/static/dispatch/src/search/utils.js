import { forEach, each, has } from "lodash"

const toPascalCase = (str) =>
  `${str}`
    .replace(new RegExp(/[-_]+/, "g"), " ")
    .replace(new RegExp(/[^\w\s]/, "g"), "")
    .replace(
      new RegExp(/\s+(.)(\w+)/, "g"),
      ($1, $2, $3) => `${$2.toUpperCase() + $3.toLowerCase()}`
    )
    .replace(new RegExp(/\s/, "g"), "")
    .replace(new RegExp(/\w/), (s) => s.toUpperCase())

export default {
  mapQueryParamsToTableOptions(options, queryParams) {
    forEach(queryParams, function (values, key) {
      if (Array.isArray(values)) {
        each(values, function (value) {
          options[key].push({ name: value })
        })
      } else {
        options[key].push({ name: values })
      }
    })
  },
  mapTableOptionsToQueryParams(options, queryParams) {
    return options, queryParams
  },
  createParametersFromTableOptions(options, rawFilters) {
    let expression = this.createFilterExpression(options.filters)
    delete options.filters

    if (!expression.length) {
      return options
    }

    if (rawFilters) {
      expression = { and: [...rawFilters, ...expression] }
    } else {
      expression = { and: expression }
    }

    return { ...options, filter: JSON.stringify(expression) }
  },
  createFilterExpression(filters) {
    let filterExpression = []
    forEach(filters, function (value, key) {
      let subFilter = []
      each(value, function (value) {
        if (has(value, "id")) {
          subFilter.push({
            model: toPascalCase(key),
            field: "id",
            op: "==",
            value: value.id,
          })
        } else if (has(value, "name")) {
          subFilter.push({
            model: toPascalCase(key),
            field: "name",
            op: "==",
            value: value.name,
          })
        } else {
          subFilter.push({ field: key, op: "==", value: value })
        }
      })
      if (subFilter.length > 0) {
        filterExpression.push({ or: subFilter })
      }
    })

    return filterExpression
  },
}