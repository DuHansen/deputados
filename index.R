install.packages("rvest")  # Só precisa uma vez
library(rvest)
library(tidyverse)
library(stringr)
 
dados_totais <- data.frame()
 
for (i in 0:9) {
  url <- paste0("https://jarbas.serenata.ai/dashboard/chamber_of_deputies/reimbursement/?p=", i)
  cat("🔎 Acessando página:", i, "\n")
  # Força o download com User-Agent pra evitar bloqueios
  pagina <- read_html(httr::GET(url, httr::user_agent("Mozilla/5.0")))
  nome <- html_elements(pagina,'.field-congressperson_name') |> html_text()
  cota <- html_elements(pagina,'.field-subquota_translated') |> html_text()
  valor_raw <- html_elements(pagina,'.field-value') |> html_text()
  valor <- as.numeric(sub(",", ".", str_extract(valor_raw, "\\-*\\d+,\\s*\\d+")))
  suspeito_raw <- html_elements(pagina,'.field-suspicious img')
  suspeito <- html_attr(suspeito_raw, "alt")
  suspeito <- tolower(suspeito) == "suspeita de irregularidade"
  # Preenche dados da página
  dados_pagina <- data.frame(
    Nome = nome,
    `Cota e Subcota` = cota,
    Valor = valor,
    Suspeito = suspeito,
    stringsAsFactors = FALSE
  )
  dados_totais <- bind_rows(dados_totais, dados_pagina)
}
 
# Visualize
View(dados_totais)
 
# Filtrar suspeitos
suspeitos <- dados_totais %>% filter(Suspeito == TRUE)
 
# Top 10 maiores valores
top_valores <- dados_totais %>% arrange(desc(Valor)) %>% head(10)
 
print(suspeitos)
print(top_valores)