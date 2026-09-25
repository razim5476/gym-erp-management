"""
Docstring for core.permissions.constants
"""


class AccountGroupPermissions:
    """
    AccountGroupPermissions
    """

    CREATE_GROUP = "accounts.create_accountgroup"
    EDIT_GROUP = "accounts.edit_accountgroup"
    VIEW_GROUP = "accounts.view_accountgroup"
    DISABLE_GROUP = "accounts.disable_accountgroup"
    DELETE_GROUP = "accounts.delete_accountsgroup"
    EXPORT_GROUP = "accounts.exportaccountgroup"
    IMPORT_GROUP = "accounts.importaccountgroup"


class AccountPermissions:
    """
    AccountPermissions
    """

    CREATE_ACCOUNT = "accounts.create_account"
    EDIT_ACCOUNT = "accounts.edit_account"
    VIEW_ACCOUNT = "accounts.view_account"
    DISABLE_ACCOUNT = "accounts.disable_account"
    DELETE_ACCOUNT = "accounts.delete_account"
    EXPORT_ACCOUNT = "accounts.exportaccount"
    IMPORT_ACCOUNT = "accounts.importaccount"



class CompanyPermissions:
    """
    CompanyPermissions
    """

    CREATE_COMPANY = "organizations.create_company"
    EDIT_COMPANY = "organizations.edit_company"
    VIEW_COMPANY = "organizations.view_company"
    DISABLE_COMPANY = "organizations.disable_company"
    DELETE_COMPANY = "organizations.delete_company"
    EXPORT_COMPANY = "organizations.exportcompany"
    IMPORT_COMPANY = "organizations.importcompany"



class BrandPermissions:
    """
    BrandPermissions
    """

    CREATE_BRAND = "core.create_brand"
    EDIT_BRAND = "core.edit_brand"
    VIEW_BRAND = "core.view_brand"
    DISABLE_BRAND = "core.disable_brand"
    DELETE_BRAND = "core.delete_brand"
    EXPORT_BRAND = "core.exportbrand"
    IMPORT_BRAND = "core.importbrand"


class CategoryPermissions:
    """
    CategoryPermissions
    """

    CREATE_CATEGORY = "core.create_category"
    EDIT_CATEGORY = "core.edit_category"
    VIEW_CATEGORY = "core.view_category"
    DISABLE_CATEGORY = "core.disable_category"
    DELETE_CATEGORY = "core.delete_category"
    EXPORT_CATEGORY = "core.exportcategory"
    IMPORT_CATEGORY = "core.importcategory"


class CountryPermissions:
    """
    CountryPermissions
    """

    CREATE_COUNTRY = "core.create_country"
    EDIT_COUNTRY = "core.edit_country"
    VIEW_COUNTRY = "core.view_country"
    DISABLE_COUNTRY = "core.disable_country"
    DELETE_COUNTRY = "core.delete_country"
    EXPORT_COUNTRY = "core.exportcountry"
    IMPORT_COUNTRY = "core.importcountry"


class StatePermissions:
    """
    StatePermissions
    """

    CREATE_STATE = "core.create_state"
    EDIT_STATE = "core.edit_state"
    VIEW_STATE = "core.view_state"
    DISABLE_STATE = "core.disable_state"
    DELETE_STATE = "core.delete_state"
    EXPORT_STATE = "core.exportstate"
    IMPORT_STATE = "core.importstate"


class CurrencyPermissions:
    """
    CurrencyPermissions
    """

    CREATE_CURRENCY = "core.create_currency"
    EDIT_CURRENCY = "core.edit_currency"
    VIEW_CURRENCY = "core.view_currency"
    DISABLE_CURRENCY = "core.disable_currency"
    DELETE_CURRENCY = "core.delete_currency"
    EXPORT_CURRENCY = "core.exportcurrency"
    IMPORT_CURRENCY = "core.importcurrency"


class UnitOfMeasurePermissions:
    """
    UnitOfMeasurePermissions
    """

    CREATE_UOM = "core.create_unitofmeasure"
    EDIT_UOM = "core.edit_unitofmeasure"
    VIEW_UOM = "core.view_unitofmeasure"
    DISABLE_UOM = "core.disable_unitofmeasure"
    DELETE_UOM = "core.delete_unitofmeasure"
    EXPORT_UOM = "core.exportunitofmeasure"
    IMPORT_UOM = "core.importunitofmeasure"


class SubCategoryPermissions:
    """
    SubCategoryPermissions
    """

    CREATE_SUB_CATEGORY = "core.create_subcategory"
    EDIT_SUB_CATEGORY = "core.edit_subcategory"
    VIEW_SUB_CATEGORY = "core.view_subcategory"
    DISABLE_SUB_CATEGORY = "core.disable_subcategory"
    DELETE_SUB_CATEGORY = "core.delete_subcategory"
    EXPORT_SUB_CATEGORY = "core.exportsubcategory"
    IMPORT_SUB_CATEGORY = "core.importsubcategory"


class BarcodePermissions:
    """
    BarcodePermissions
    """

    CREATE_BARCODE = "core.create_barcodes"
    EDIT_BARCODE = "core.edit_barcodes"
    VIEW_BARCODE = "core.view_barcodes"
    DISABLE_BARCODE = "core.disable_barcodes"
    DELETE_BARCODE = "core.delete_barcodes"
    EXPORT_BARCODE = "core.exportbarcodes"
    IMPORT_BARCODE = "core.importbarcodes"


class PaginationSizePermissions:
    """
    PaginationSizePermissions
    """

    CREATE_PAGINATION_SIZE = "core.create_paginationsize"
    EDIT_PAGINATION_SIZE = "core.edit_paginationsize"
    VIEW_PAGINATION_SIZE = "core.view_paginationsize"
    DISABLE_PAGINATION_SIZE = "core.disable_paginationsize"
    DELETE_PAGINATION_SIZE = "core.delete_paginationsize"
    EXPORT_PAGINATION_SIZE = "core.exportpaginationsize"
    IMPORT_PAGINATION_SIZE = "core.importpaginationsize"


class ProductCategoryPermissions:
    """
    ProductCategoryPermissions
    """

    CREATE_PRODUCT_CATEGORY = "product.create_productcategory"
    EDIT_PRODUCT_CATEGORY = "product.edit_productcategory"
    VIEW_PRODUCT_CATEGORY = "product.view_productcategory"
    DISABLE_PRODUCT_CATEGORY = "product.disable_productcategory"
    DELETE_PRODUCT_CATEGORY = "product.delete_productcategory"
    EXPORT_PRODUCT_CATEGORY = "product.exportproductcategory"
    IMPORT_PRODUCT_CATEGORY = "product.importproductcategory"


class UniqueIdPermissions:
    """
    UniqueIdPermissions
    """

    CREATE_UNIQUE_ID = "core.create_uniqueid"
    EDIT_UNIQUE_ID = "core.edit_uniqueid"
    VIEW_UNIQUE_ID = "core.view_uniqueid"
    DISABLE_UNIQUE_ID = "core.disable_uniqueid"
    DELETE_UNIQUE_ID = "core.delete_uniqueid"
    EXPORT_UNIQUE_ID = "core.exportuniqueid"
    IMPORT_UNIQUE_ID = "core.importuniqueid"


class FinancialYearPermissions:
    """
    FinancialYearPermissions
    """

    CREATE_FINANCIAL_YEAR = "core.create_financialyear"
    EDIT_FINANCIAL_YEAR = "core.edit_financialyear"
    VIEW_FINANCIAL_YEAR = "core.view_financialyear"
    DISABLE_FINANCIAL_YEAR = "core.disable_financialyear"
    DELETE_FINANCIAL_YEAR = "core.delete_financialyear"
    EXPORT_FINANCIAL_YEAR = "core.exportfinancialyear"
    IMPORT_FINANCIAL_YEAR = "core.importfinancialyear"


class PaymentMethodPermissions:
    """
    PaymentMethodPermissions
    """

    CREATE_PAYMENT_METHOD = "accounts.create_paymentmethod"
    EDIT_PAYMENT_METHOD = "accounts.edit_paymentmethod"
    VIEW_PAYMENT_METHOD = "accounts.view_paymentmethod"
    DISABLE_PAYMENT_METHOD = "accounts.disable_paymentmethod"
    DELETE_PAYMENT_METHOD = "accounts.delete_paymentmethod"
    EXPORT_PAYMENT_METHOD = "accounts.exportpaymentmethod"
    IMPORT_PAYMENT_METHOD = "accounts.importpaymentmethod"


class CustomerGroupPermissions:
    """CustomerGroupPermissions"""
    CREATE_CUSTOMER_GROUP = "registrations.create_customergroup"
    EDIT_CUSTOMER_GROUP = "registrations.edit_customergroup"
    VIEW_CUSTOMER_GROUP = "registrations.view_customergroup"
    DISABLE_CUSTOMER_GROUP = "registrations.disable_customergroup"
    DELETE_CUSTOMER_GROUP = "registrations.delete_customergroup"
    EXPORT_CUSTOMER_GROUP = "registrations.exportcustomergroup"
    IMPORT_CUSTOMER_GROUP = "registrations.importcustomergroup"


class CustomerPermissions:
    """CustomerPermissions"""
    CREATE_CUSTOMER = "registrations.create_customer"
    EDIT_CUSTOMER = "registrations.edit_customer"
    VIEW_CUSTOMER = "registrations.view_customer"
    DISABLE_CUSTOMER = "registrations.disable_customer"
    DELETE_CUSTOMER = "registrations.delete_customer"
    EXPORT_CUSTOMER = "registrations.exportcustomer"
    IMPORT_CUSTOMER = "registrations.importcustomer"


class SupplierGroupPermissions:
    """SupplierGroupPermissions"""
    CREATE_SUPPLIER_GROUP = "registrations.create_suppliergroup"
    EDIT_SUPPLIER_GROUP = "registrations.edit_suppliergroup"
    VIEW_SUPPLIER_GROUP = "registrations.view_suppliergroup"
    DISABLE_SUPPLIER_GROUP = "registrations.disable_suppliergroup"
    DELETE_SUPPLIER_GROUP = "registrations.delete_suppliergroup"
    EXPORT_SUPPLIER_GROUP = "registrations.exportsuppliergroup"
    IMPORT_SUPPLIER_GROUP = "registrations.importsuppliergroup"


class SupplierPermissions:
    """SupplierPermissions"""
    CREATE_SUPPLIER = "registrations.create_supplier"
    EDIT_SUPPLIER = "registrations.edit_supplier"
    VIEW_SUPPLIER = "registrations.view_supplier"
    DISABLE_SUPPLIER = "registrations.disable_supplier"
    DELETE_SUPPLIER = "registrations.delete_supplier"
    EXPORT_SUPPLIER = "registrations.exportsupplier"
    IMPORT_SUPPLIER = "registrations.importsupplier"
