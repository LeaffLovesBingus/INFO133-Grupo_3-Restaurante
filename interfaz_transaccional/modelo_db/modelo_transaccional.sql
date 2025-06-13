CREATE TABLE "Ventas" (
  "Id_Venta" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Cantidad_Productos" integer,
  "Monto_Total" integer,
  "Fecha_Venta" timestamp,
  "FK_Id_Mesero" integer NOT NULL,
  "FK_Id_Mesa" integer NOT NULL,
  "FK_Id_Medio_Pago" integer NOT NULL
);

CREATE TABLE "Mesas" (
  "Id_Mesa" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Capacidad" integer
);

CREATE TABLE "reservas" (
  "PK_id_reservas" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "FK_id_mesas" integer NOT NULL,
  "estado_reserva" varchar,
  "fecha_reserva" timestamp,
  "nombre_cliente" varchar,
  "telefono_cliente" varchar
);

CREATE TABLE "Medio_Pago" (
  "Id_Medio_Pago" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Medio_Pago" varchar
);

CREATE TABLE "Consumibles_Vendidos" (
  "FK_Id_Venta" integer NOT NULL,
  "FK_Id_Consumible" integer NOT NULL,
  "Cantidad" integer
);

CREATE TABLE "Consumibles" (
  "Id_consumibles" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Nombre" varchar,
  "Precio_unidad" integer,
  "Categoria" varchar
);

CREATE TABLE "Cocinero" (
  "Id_cocinero" integer UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE "Mesero" (
  "Id_mesero" integer UNIQUE NOT NULL GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE "Empleados" (
  "Id_empleado" integer UNIQUE PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Nombre" varchar,
  "Apellido" varchar,
  "Correo" varchar,
  "Sueldo" integer
);

CREATE TABLE "Ingredientes" (
  "Id_ingrediente" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "Nombre" varchar,
  "Tipo" varchar,
  "Cantidad" integer
);

CREATE TABLE "Ingredientes_Usados" (
  "Id_Ingredientes_Usados" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "FK_Id_consumible" integer NOT NULL,
  "FK_Id_ingrediente" integer NOT NULL,
  "Cantidad" integer,
  "Fecha_uso" timestamp,
  "FK_Id_cocinero" integer NOT NULL
);

ALTER TABLE "Ventas" ADD FOREIGN KEY ("FK_Id_Mesero") REFERENCES "Mesero" ("Id_mesero");

ALTER TABLE "Ventas" ADD FOREIGN KEY ("FK_Id_Mesa") REFERENCES "Mesas" ("Id_Mesa");

ALTER TABLE "Ventas" ADD FOREIGN KEY ("FK_Id_Medio_Pago") REFERENCES "Medio_Pago" ("Id_Medio_Pago");

ALTER TABLE "reservas" ADD FOREIGN KEY ("FK_id_mesas") REFERENCES "Mesas" ("Id_Mesa");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_Id_Venta") REFERENCES "Ventas" ("Id_Venta");

ALTER TABLE "Consumibles_Vendidos" ADD FOREIGN KEY ("FK_Id_Consumible") REFERENCES "Consumibles" ("Id_consumibles");

ALTER TABLE "Cocinero" ADD FOREIGN KEY ("Id_cocinero") REFERENCES "Empleados" ("Id_empleado");

ALTER TABLE "Mesero" ADD FOREIGN KEY ("Id_mesero") REFERENCES "Empleados" ("Id_empleado");

ALTER TABLE "Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_consumible") REFERENCES "Consumibles" ("Id_consumibles");

ALTER TABLE "Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_ingrediente") REFERENCES "Ingredientes" ("Id_ingrediente");

ALTER TABLE "Ingredientes_Usados" ADD FOREIGN KEY ("FK_Id_cocinero") REFERENCES "Cocinero" ("Id_cocinero");
