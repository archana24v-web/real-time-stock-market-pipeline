terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "pipeline_rg" {
  name     = "stock-pipeline-rg"
  location = "East US"
}

resource "azurerm_storage_account" "adls" {
  name                     = "stockpipelineadls"
  resource_group_name      = azurerm_resource_group.pipeline_rg.name
  location                 = azurerm_resource_group.pipeline_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true  # Enables ADLS Gen2
}

resource "azurerm_synapse_workspace" "synapse" {
  name                                 = "stock-synapse-ws"
  resource_group_name                  = azurerm_resource_group.pipeline_rg.name
  location                             = azurerm_resource_group.pipeline_rg.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_account.adls.id
  sql_administrator_login              = "sqladmin"
  sql_administrator_login_password     = var.sql_password
}
