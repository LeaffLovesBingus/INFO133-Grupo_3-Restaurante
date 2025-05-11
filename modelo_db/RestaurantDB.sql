CREATE TABLE "Hechos_Ventas" (
  "PK_ID_Venta" integer,
  "Cantidad_Productos" integer,
  "Monto_Total" integer,
  "Fecha_Venta" timestamp,
  "FK_Id_Mesero" integer UNIQUE NOT NULL,
  "FK_Id_Mesa" integer,
  "Medio_Pago" integer UNIQUE NOT NULL,
  PRIMARY KEY ("PK_ID_Venta", "FK_Id_Mesa"),
  UNIQUE ("PK_ID_Venta")
);

CREATE TABLE "Medio_Pago" (
  "PK_ID_Medio_Pago" integer PRIMARY KEY,
  "Medio_Pago" varchar
);

CREATE TABLE "Consumibles_Vendidos" (
  "FK_ID_Venta" integer UNIQUE NOT NULL,
  "FK_ID_Consumible" integer UNIQUE NOT NULL,
  "Cantidad" integer
);

CREATE TABLE "Consumibles" (
  "PK_id_consumibles" integer PRIMARY KEY,
  "Nombre" varchar,
  "Precio_unidad" integer,
  "Categoria" varchar
);

CREATE TABLE "Cocinero" (
  "FK_id_cocinero" integer PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Correo" varchar,
  "Sueldo" integer
);

CREATE TABLE "Mesero" (
  "FK_id_mesero" integer PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Correo" varchar,
  "Sueldo" integer
);

CREATE TABLE "Ingredientes" (
  "PK_id_ingrediente" integer PRIMARY KEY,
  "Nombre" varchar,
  "Tipo" varchar,
  "Cantidad" integer
);

CREATE TABLE "Hechos_Ingredientes_Usados" (
  "PK_Id_Ingredientes_Usados" integer PRIMARY KEY,
  "FK_id_consumible" integer UNIQUE NOT NULL,
  "FK_id_ingrediente" integer UNIQUE NOT NULL,
  "Cantidad" integer,
  "Fecha_uso" timestamp,
  "FK_id_cocinero" integer UNIQUE NOT NULL
);

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("FK_Id_Mesero") REFERENCES "Mesero" ("FK_id_mesero");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("Medio_Pago") REFERENCES "Medio_Pago" ("PK_ID_Medio_Pago");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_ID_Venta") REFERENCES "Hechos_Ventas" ("PK_ID_Venta");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_ID_Consumible") REFERENCES "Consumibles" ("PK_id_consumibles");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_id_consumible") REFERENCES "Consumibles" ("PK_id_consumibles");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_id_ingrediente") REFERENCES "Ingredientes" ("PK_id_ingrediente");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_id_cocinero") REFERENCES "Cocinero" ("FK_id_cocinero");
