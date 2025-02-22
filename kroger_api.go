package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  url := "https://api.kroger.com/v1/products?filter.brand={{Kroger}}&filter.term={{apples}}&filter.locationId={{LOCATION_ID}}"

  req, _ := http.NewRequest("GET", url, nil)

  req.Header.Add("Accept", "application/json")
  req.Header.Add("Authorization", "Bearer {{LgSIyTGKumUF5KJwuMIc4yP0QF_8uQ0gpZwObxiR}}")

  res, _ := http.DefaultClient.Do(req)

  defer res.Body.Close()
  body, _ := ioutil.ReadAll(res.Body)

  fmt.Println(res)
  fmt.Println(string(body))

}
