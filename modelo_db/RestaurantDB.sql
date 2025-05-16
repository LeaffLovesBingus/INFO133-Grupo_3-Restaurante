CREATE TABLE "Hechos_Ventas" (
  "Id_Venta" integer,
  "Cantidad_Productos" integer,
  "Cantidad_clientes" integer,
  "Monto_Total" integer,
  "Fecha_Venta" timestamp,
  "FK_Id_Mesero" integer NOT NULL,
  "Id_Mesa" integer,
  "FK_Id_Medio_Pago" integer NOT NULL,
  PRIMARY KEY ("Id_Venta")
);

CREATE TABLE "Medio_Pago" (
  "Id_Medio_Pago" integer PRIMARY KEY,
  "Medio_Pago" varchar
);

CREATE TABLE "Consumibles_Vendidos" (
  "FK_Id_Venta" integer NOT NULL,
  "FK_Id_Consumible" integer NOT NULL,
  "Cantidad" integer
);

CREATE TABLE "Consumibles" (
  "Id_consumibles" integer PRIMARY KEY,
  "Nombre" varchar,
  "Precio_unidad" integer,
  "Categoria" varchar
);

CREATE TABLE "Cocinero" (
  "Id_cocinero" integer PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Correo" varchar,
  "Sueldo" integer
);

CREATE TABLE "Mesero" (
  "Id_mesero" integer PRIMARY KEY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Correo" varchar,
  "Sueldo" integer
);

CREATE TABLE "Ingredientes" (
  "Id_ingrediente" integer PRIMARY KEY,
  "Nombre" varchar,
  "Tipo" varchar,
  "Cantidad" integer
);

CREATE TABLE "Hechos_Ingredientes_Usados" (
  "Id_Ingredientes_Usados" integer PRIMARY KEY,
  "FK_Id_consumible" integer NOT NULL,
  "FK_Id_ingrediente" integer NOT NULL,
  "Cantidad" integer,
  "Fecha_uso" timestamp,
  "FK_Id_cocinero" integer NOT NULL
);


ALTER TABLE "Hechos_Ventas" ALTER COLUMN "Id_Venta" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Medio_Pago" ALTER COLUMN "Id_Medio_Pago" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Consumibles" ALTER COLUMN "Id_consumibles" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Cocinero" ALTER COLUMN "Id_cocinero" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Mesero" ALTER COLUMN "Id_mesero" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Ingredientes" ALTER COLUMN "Id_ingrediente" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Hechos_Ingredientes_Usados" ALTER COLUMN "Id_Ingredientes_Usados" ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("FK_Id_Mesero") REFERENCES "Mesero" ("Id_mesero");

ALTER TABLE "Hechos_Ventas" ADD FOREIGN KEY ("FK_Id_Medio_Pago") REFERENCES "Medio_Pago" ("Id_Medio_Pago");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_Id_Venta") REFERENCES "Hechos_Ventas" ("Id_Venta");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_Id_Consumible") REFERENCES "Consumibles" ("Id_consumibles");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_consumible") REFERENCES "Consumibles" ("Id_consumibles");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_ingrediente") REFERENCES "Ingredientes" ("Id_ingrediente");

ALTER TABLE "Hechos_Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_cocinero") REFERENCES "Cocinero" ("Id_cocinero");
