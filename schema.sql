-- 
-- LH Nautical - Geraçao do PostGreSQl a partir de CSVs
-- Total Tables: 24
-- 

-- Table: addresses
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    address_type VARCHAR(50),
    postal_code VARCHAR(50),
    street VARCHAR(50),
    number INTEGER,
    complement VARCHAR(50),
    district VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    is_primary BOOLEAN
);

-- Table: attributes
CREATE TABLE IF NOT EXISTS attributes (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    data_type VARCHAR(50)
);

-- Table: brands
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    country VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: categories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    slug VARCHAR(50),
    parent_category_id INTEGER,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: customers
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    person_type VARCHAR(50),
    legal_name VARCHAR(50),
    trade_name VARCHAR(50),
    tax_id BIGINT,
    state_registration VARCHAR(50),
    email VARCHAR(50),
    phone VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: employees
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR(50),
    cpf BIGINT,
    email VARCHAR(50),
    role VARCHAR(50),
    primary_location_id INTEGER,
    hire_date DATE,
    termination_date DATE,
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: fiscal_invoices
CREATE TABLE IF NOT EXISTS fiscal_invoices (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    nfe_number VARCHAR(50),
    nfe_access_key BIGINT,
    series INTEGER,
    issued_at TIMESTAMP,
    status VARCHAR(50),
    total_amount NUMERIC(15, 2),
    xml_storage_uri VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: goods_receipt_items
CREATE TABLE IF NOT EXISTS goods_receipt_items (
    id INTEGER PRIMARY KEY,
    goods_receipt_id INTEGER,
    purchase_order_item_id INTEGER,
    quantity_received NUMERIC(15, 2)
);

-- Table: goods_receipts
CREATE TABLE IF NOT EXISTS goods_receipts (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER,
    received_by_employee_id INTEGER,
    received_at TIMESTAMP,
    notes VARCHAR(50),
    created_at TIMESTAMP
);

-- Table: locations
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    location_type VARCHAR(50),
    postal_code VARCHAR(50),
    street VARCHAR(50),
    number INTEGER,
    complement VARCHAR(50),
    district VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: order_items
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_variant_id INTEGER,
    quantity INTEGER,
    unit_price NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

-- Table: orders
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    order_number VARCHAR(50),
    channel VARCHAR(50),
    customer_id INTEGER,
    salesperson_id INTEGER,
    location_id INTEGER,
    status VARCHAR(50),
    subtotal NUMERIC(15, 2),
    discount_amount NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: payments
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    method VARCHAR(50),
    installments INTEGER,
    amount NUMERIC(15, 2),
    status VARCHAR(50),
    paid_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: product_suppliers
CREATE TABLE IF NOT EXISTS product_suppliers (
    product_variant_id INTEGER,
    supplier_id INTEGER,
    supplier_sku VARCHAR(50),
    last_quoted_cost NUMERIC(15, 2),
    lead_time_days INTEGER,
    is_preferred BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: product_variants
CREATE TABLE IF NOT EXISTS product_variants (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    sku VARCHAR(50),
    barcode_ean BIGINT,
    sale_price NUMERIC(15, 2),
    cost_price NUMERIC(15, 2),
    weight_kg NUMERIC(15, 2),
    icms_rate NUMERIC(15, 2),
    ipi_rate NUMERIC(15, 2),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: products
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    description VARCHAR(50),
    brand_id INTEGER,
    category_id INTEGER,
    ncm_code INTEGER,
    unit_of_measure VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: purchase_order_items
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id INTEGER PRIMARY KEY,
    purchase_order_id INTEGER,
    product_variant_id INTEGER,
    quantity_ordered INTEGER,
    unit_cost NUMERIC(15, 2),
    line_total NUMERIC(15, 2)
);

-- Table: purchase_orders
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER PRIMARY KEY,
    po_number VARCHAR(50),
    supplier_id INTEGER,
    buyer_id INTEGER,
    destination_location_id INTEGER,
    status VARCHAR(50),
    currency VARCHAR(50),
    subtotal NUMERIC(15, 2),
    total NUMERIC(15, 2),
    placed_at TIMESTAMP,
    expected_delivery_at DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: return_items
CREATE TABLE IF NOT EXISTS return_items (
    id INTEGER PRIMARY KEY,
    return_id INTEGER,
    order_item_id INTEGER,
    quantity NUMERIC(15, 2),
    action VARCHAR(50),
    exchange_variant_id INTEGER,
    unit_refund_amount NUMERIC(15, 2)
);

-- Table: returns
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY,
    return_number VARCHAR(50),
    order_id INTEGER,
    customer_id INTEGER,
    received_at_location_id INTEGER,
    status VARCHAR(50),
    reason VARCHAR(50),
    total_refund_amount NUMERIC(15, 2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: stock_levels
CREATE TABLE IF NOT EXISTS stock_levels (
    product_variant_id INTEGER,
    location_id INTEGER,
    quantity_on_hand NUMERIC(15, 2),
    reorder_point TEXT,
    updated_at TIMESTAMP
);

-- Table: stock_movements
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY,
    product_variant_id INTEGER,
    location_id INTEGER,
    movement_type VARCHAR(50),
    quantity NUMERIC(15, 2),
    reference_table TEXT,
    reference_id TEXT,
    employee_id TEXT,
    notes VARCHAR(50),
    occurred_at TIMESTAMP,
    created_at TIMESTAMP
);

-- Table: suppliers
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY,
    legal_name VARCHAR(50),
    trade_name VARCHAR(50),
    country VARCHAR(50),
    tax_id VARCHAR(50),
    tax_id_type VARCHAR(50),
    email VARCHAR(50),
    phone BIGINT,
    contact_name VARCHAR(50),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: variant_attribute_values
CREATE TABLE IF NOT EXISTS variant_attribute_values (
    product_variant_id INTEGER,
    attribute_id INTEGER,
    value VARCHAR(50)
);
