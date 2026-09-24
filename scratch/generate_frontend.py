import os

html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Retenciones - Gestión Fiscal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        brand: {
                            sidebar: '#48B8B8',     // Turquesa de las imágenes
                            background: '#FFF9E6',  // Marfil/Crema suave
                            primary: '#F08060',     // Coral/Naranja suave
                            primaryHover: '#E07151',
                            yellowBg: '#FDE68A',    // Amarillo suave para badges y banners
                            yellowText: '#8C730A',
                            text: '#2C3E50',
                        }
                    },
                    fontFamily: {
                        sans: ['Outfit', 'Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        body { background-color: #FFF9E6; font-family: 'Outfit', 'Inter', sans-serif; }
        .nav-btn.active {
            background-color: white !important;
            color: #2C3E50 !important;
            box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.08);
        }
        input[type=number]::-webkit-inner-spin-button, 
        input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
        input[type=number] { -moz-appearance: textfield; }
        
        .input-base {
            width: 100%;
            padding: 0.65rem 1rem;
            border-radius: 0.85rem;
            border: 1px solid #E2E8F0;
            background-color: #FFFFFF;
            color: #334155;
            outline: none;
            transition: all 0.2s ease;
        }
        .input-base:focus {
            border-color: #F08060;
            box-shadow: 0 0 0 3px rgba(240, 128, 96, 0.15);
        }
        .label-base {
            display: block;
            font-size: 0.85rem;
            font-weight: 700;
            color: #475569;
            margin-bottom: 0.4rem;
        }
        .btn-coral {
            background-color: #F08060;
            color: white;
            font-weight: 700;
            border-radius: 0.85rem;
            padding: 0.65rem 1.25rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(240, 128, 96, 0.25);
            display: inline-flex;
            items-center: center;
            justify-content: center;
            gap: 0.5rem;
        }
        .btn-coral:hover {
            background-color: #E07151;
            transform: translateY(-1px);
        }
        .btn-outline {
            background-color: white;
            color: #475569;
            font-weight: 700;
            border-radius: 0.85rem;
            padding: 0.65rem 1.25rem;
            border: 1px solid #CBD5E1;
            transition: all 0.2s ease;
        }
        .btn-outline:hover {
            background-color: #F8FAFC;
            color: #1E293B;
        }
        .badge-yellow {
            background-color: #FDE68A;
            color: #8C730A;
            font-weight: 700;
            padding: 0.2rem 0.65rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            display: inline-block;
        }
    </style>
</head>
<body class="h-screen flex overflow-hidden text-brand-text">

    <!-- SIDEBAR -->
    <aside class="w-64 bg-brand-sidebar text-white flex flex-col shadow-2xl z-20">
        <div class="p-6 flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-black tracking-tight">RETENCIONES</h1>
                <p class="text-white/80 text-xs font-medium mt-0.5">Gestión Fiscal</p>
            </div>
            <button class="text-white/70 hover:text-white"><i class="fa-solid fa-chevron-left text-sm"></i></button>
        </div>

        <nav id="sidebar-nav" class="flex-1 px-4 py-4 space-y-2.5 mt-2">
            <button id="nav-view-historial-retenciones" onclick="switchView('view-historial-retenciones')" class="nav-btn active w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-file-invoice w-5 text-center"></i> Retenciones
            </button>
            <button id="nav-view-proveedores" onclick="switchView('view-proveedores')" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-users w-5 text-center"></i> Proveedores
            </button>
            <button id="nav-view-documentos" onclick="switchView('view-documentos')" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-shield-halved w-5 text-center"></i> Autorizaciones (CAI)
            </button>
            <button id="nav-view-empresa" onclick="switchView('view-empresa')" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-building w-5 text-center"></i> Mi Empresa
            </button>
            <button id="nav-view-usuarios" onclick="switchView('view-usuarios')" class="nav-btn w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-user-shield w-5 text-center"></i> Usuarios
            </button>
        </nav>

        <div class="p-4 border-t border-white/10">
            <button onclick="showToast('Sesión finalizada', 'success')" class="w-full flex items-center gap-3 px-4 py-3 rounded-2xl transition-all font-semibold text-white/90 hover:bg-white/10 hover:text-white">
                <i class="fa-solid fa-arrow-right-from-bracket w-5 text-center"></i> Cerrar Sesión
            </button>
        </div>
    </aside>

    <!-- MAIN CONTAINER -->
    <main class="flex-1 overflow-y-auto relative">
        <div class="max-w-7xl mx-auto p-8 relative">

            <!-- ========================================== -->
            <!-- VISTA: HISTORIAL RETENCIONES               -->
            <!-- ========================================== -->
            <section id="view-historial-retenciones" class="view-section">
                <div class="flex justify-between items-end mb-6">
                    <div>
                        <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Retenciones</h2>
                        <p class="text-slate-500 text-sm font-medium mt-1">Bienvenido, <strong>Breidy Funes</strong></p>
                    </div>
                </div>

                <!-- Buscador Avanzado y Botón Nuevo -->
                <div class="flex items-center justify-between mb-6 bg-white p-3 rounded-2xl shadow-sm border border-slate-100 gap-4">
                    <div class="relative flex-1">
                        <i class="fa-solid fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
                        <input type="text" id="filtroBusquedaGlobal" class="w-full pl-11 pr-4 py-2.5 bg-slate-50 rounded-xl text-sm border-none focus:ring-0 outline-none placeholder:text-slate-400" placeholder="Buscar por proveedor, RTN o No. retención...">
                    </div>
                    <button onclick="abrirModalRetencion()" class="btn-coral text-sm whitespace-nowrap">
                        <i class="fa-solid fa-plus"></i> Nueva Retención
                    </button>
                </div>

                <!-- Tabla de Historial -->
                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-slate-50/70 border-b border-slate-100 text-[11px] uppercase tracking-wider text-slate-400 font-bold">
                                    <th class="py-4 px-6">N° Retención</th>
                                    <th class="py-4 px-6">Fecha</th>
                                    <th class="py-4 px-6">Proveedor</th>
                                    <th class="py-4 px-6 text-right">Monto Retenido</th>
                                    <th class="py-4 px-6 text-center">Acciones</th>
                                </tr>
                            </thead>
                            <tbody id="tabla-retenciones"></tbody>
                        </table>
                    </div>
                    <div id="empty-state" class="hidden py-16 text-center flex flex-col items-center">
                        <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center text-slate-300 mb-4">
                            <i class="fa-solid fa-file-invoice text-3xl"></i>
                        </div>
                        <h3 class="text-slate-600 font-medium">No hay retenciones registradas</h3>
                    </div>
                    <!-- Paginación Retenciones -->
                    <div id="paginacion-retenciones-container" class="p-4 bg-slate-50/70 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-semibold text-slate-500">
                        <div id="paginacion-info-retenciones">Mostrando 1 a 10 de 12 retenciones</div>
                        <div class="flex items-center gap-1.5" id="paginacion-botones-retenciones"></div>
                    </div>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- VISTA: PROVEEDORES                         -->
            <!-- ========================================== -->
            <section id="view-proveedores" class="view-section hidden">
                <div class="flex justify-between items-center mb-6">
                    <div>
                        <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Proveedores</h2>
                        <p class="text-slate-500 text-sm font-medium mt-1">Bienvenido, <strong>Breidy Funes</strong></p>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="relative">
                            <i class="fa-solid fa-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
                            <input type="text" id="searchRTNProv" class="pl-9 pr-4 py-2 rounded-xl border border-slate-200 text-sm focus:border-brand-primary outline-none w-64 bg-white shadow-sm" placeholder="Buscar por nombre o RTN...">
                        </div>
                        <button onclick="abrirModalProveedor()" class="btn-coral text-sm">
                            <i class="fa-solid fa-plus"></i> Nuevo Proveedor
                        </button>
                    </div>
                </div>

                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/70 border-b border-slate-100 text-[11px] uppercase tracking-wider text-slate-400 font-bold">
                                <th class="py-4 px-6">Proveedor</th>
                                <th class="py-4 px-6">RTN</th>
                                <th class="py-4 px-6">Contacto</th>
                                <th class="py-4 px-6">Teléfono / Correo</th>
                                <th class="py-4 px-6 text-center">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="tabla-proveedores"></tbody>
                    </table>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- VISTA: DOCUMENTOS CAI                      -->
            <!-- ========================================== -->
            <section id="view-documentos" class="view-section hidden">
                <div class="flex justify-between items-center mb-6">
                    <div>
                        <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Autorizaciones (CAI)</h2>
                        <p class="text-slate-500 text-sm font-medium mt-1">Gestión de Talonarios Fiscales SAR</p>
                    </div>
                    <button onclick="abrirModalDocumento()" class="btn-coral text-sm">
                        <i class="fa-solid fa-plus"></i> Nuevo CAI
                    </button>
                </div>

                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/70 border-b border-slate-100 text-[11px] uppercase tracking-wider text-slate-400 font-bold">
                                <th class="py-4 px-6">Prefijo</th>
                                <th class="py-4 px-6">Rango Autorizado</th>
                                <th class="py-4 px-6">Clave CAI</th>
                                <th class="py-4 px-6">Vencimiento</th>
                                <th class="py-4 px-6 text-center">Último Usado</th>
                                <th class="py-4 px-6 text-center">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="tabla-documentos"></tbody>
                    </table>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- VISTA: MI EMPRESA                          -->
            <!-- ========================================== -->
            <section id="view-empresa" class="view-section hidden">
                <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight mb-6">Mi Empresa</h2>
                <div class="max-w-2xl">
                    <div class="bg-white rounded-3xl shadow-sm border border-slate-100 p-8">
                        <form id="empresaForm" class="space-y-5">
                            <input type="hidden" id="emp_id" value="1">
                            <div>
                                <label class="label-base">RTN de la Empresa <span class="text-brand-primary">*</span></label>
                                <input type="text" id="emp_RTN" required class="input-base" maxlength="14" placeholder="00000000000000">
                            </div>
                            <div>
                                <label class="label-base">Nombre / Razón Social <span class="text-brand-primary">*</span></label>
                                <input type="text" id="emp_empresa" required class="input-base" placeholder="Nombre de tu empresa">
                            </div>
                            <div>
                                <label class="label-base">Dirección</label>
                                <input type="text" id="emp_direccion" class="input-base" placeholder="Dirección de la empresa">
                            </div>
                            <div>
                                <label class="label-base">Teléfono</label>
                                <input type="text" id="emp_telefono" class="input-base" placeholder="Teléfono de contacto">
                            </div>
                            <div class="flex justify-end pt-4">
                                <button type="submit" class="btn-coral">Actualizar Datos</button>
                            </div>
                        </form>
                    </div>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- VISTA: USUARIOS                            -->
            <!-- ========================================== -->
            <section id="view-usuarios" class="view-section hidden">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Usuarios</h2>
                    <button onclick="abrirModalUsuario()" class="btn-coral text-sm">
                        <i class="fa-solid fa-plus"></i> Nuevo Usuario
                    </button>
                </div>
                <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-50/70 border-b border-slate-100 text-[11px] uppercase tracking-wider text-slate-400 font-bold">
                                <th class="py-4 px-6">ID</th>
                                <th class="py-4 px-6">Usuario</th>
                                <th class="py-4 px-6">Nombre Completo</th>
                                <th class="py-4 px-6 text-center">Rol</th>
                                <th class="py-4 px-6 text-center">Acciones</th>
                            </tr>
                        </thead>
                        <tbody id="tabla-usuarios"></tbody>
                    </table>
                </div>
            </section>

        </div>
    </main>

    <!-- ================================================================= -->
    <!-- MODAL: NUEVA / EDITAR RETENCIÓN (COMO IMÁGENES 2 Y 3)              -->
    <!-- ================================================================= -->
    <div id="modal-retenciones" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto hidden">
        <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-2xl max-h-[92vh] overflow-y-auto relative animate-in fade-in zoom-in-95 duration-200">
            <!-- Botón Cerrar "X" -->
            <button type="button" onclick="closeModal('modal-retenciones')" class="absolute top-6 right-6 text-slate-400 hover:text-slate-600 text-xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100 transition-colors">
                <i class="fa-solid fa-xmark"></i>
            </button>

            <!-- Encabezado Modal -->
            <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-xl bg-brand-primary/10 text-brand-primary flex items-center justify-center text-xl">
                    <i class="fa-solid fa-file-circle-plus"></i>
                </div>
                <h3 id="form-title-retenciones" class="text-2xl font-extrabold text-slate-800">Nueva Retención</h3>
            </div>

            <!-- Banner Amarillo NÚMERO DE RETENCIÓN & CAI (Exacto Imagen 3) -->
            <div id="cai_alert" class="bg-brand-yellowBg text-brand-yellowText rounded-2xl p-5 mb-6 shadow-sm border border-amber-200/60 relative">
                <button type="button" onclick="evaluarCAIActivo()" class="absolute top-4 right-4 text-brand-yellowText hover:opacity-75 transition-opacity text-sm">
                    <i class="fa-solid fa-arrows-rotate"></i>
                </button>
                <div class="text-[11px] font-bold uppercase tracking-wider text-amber-800/80 mb-1">
                    NÚMERO DE RETENCIÓN
                </div>
                <div class="text-3xl font-black tracking-tight text-slate-900 mb-1" id="num_doc_display">
                    563
                </div>
                <div class="text-xs font-medium text-amber-900/90">
                    CAI: <span id="cai_display">48C542-CBC560-880DE0-63BE03-090937-71</span> · Rango: <span id="rango_display">1 - 1000</span>
                </div>
            </div>

            <form id="retencionForm" class="space-y-6">
                <input type="hidden" id="retencion_id">
                <input type="hidden" id="documento_id">
                <input type="hidden" id="num_documento_oculto">
                <input type="hidden" id="proveedor_id">

                <!-- Fecha de Retención -->
                <div>
                    <label class="label-base flex items-center gap-2"><i class="fa-regular fa-calendar text-slate-400"></i> Fecha de Retención</label>
                    <input type="date" id="fecha" required class="input-base font-medium">
                </div>

                <!-- Proveedor Combobox -->
                <div class="relative">
                    <label class="label-base flex items-center gap-2"><i class="fa-solid fa-building-user text-slate-400"></i> Proveedor</label>
                    <div class="relative">
                        <i class="fa-solid fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-sm pointer-events-none"></i>
                        <input type="text" id="proveedor_search" class="input-base pl-11 pr-10 cursor-text" placeholder="Buscar proveedor por nombre o RTN..." autocomplete="off">
                        <i class="fa-solid fa-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs transition-transform duration-200 pointer-events-none" id="proveedor_icon"></i>
                    </div>
                    <div id="proveedor_dropdown" class="absolute z-50 w-full mt-1 bg-white border border-slate-200 rounded-2xl shadow-2xl hidden max-h-60 overflow-y-auto">
                        <div class="px-4 py-2 bg-brand-sidebar text-white text-xs font-bold sticky top-0 z-10">Seleccione el proveedor...</div>
                        <ul id="proveedor_list" class="py-1 text-sm text-slate-700"></ul>
                    </div>
                </div>

                <!-- PANEL DATOS DE LA FACTURA -->
                <div class="bg-slate-50/80 rounded-2xl p-6 border border-slate-200/80 space-y-4">
                    <div class="flex items-center gap-2 text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">
                        <i class="fa-solid fa-file-lines text-brand-primary"></i> DATOS DE LA FACTURA
                    </div>
                    <div>
                        <label class="label-base">Fecha de Factura</label>
                        <input type="date" id="Fecha_factura" class="input-base">
                    </div>
                    <div>
                        <label class="label-base">Número de Factura</label>
                        <input type="text" id="Num_factura" required class="input-base font-mono" placeholder="000-000-01-00000000" maxlength="19">
                        <div id="cont-fac" class="text-[11px] font-medium text-red-600 mt-1">Caracteres: 0 / 19</div>
                    </div>
                    <div>
                        <label class="label-base">CAI de la Factura</label>
                        <input type="text" id="CAI_factura" required class="input-base font-mono uppercase" placeholder="XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XX" maxlength="37">
                        <div id="cont-cai" class="text-[11px] font-medium text-red-600 mt-1">Caracteres: 0 / 37</div>
                    </div>
                </div>

                <!-- Tipo de Impuesto (ISR vs IVA tabs) -->
                <div>
                    <label class="label-base flex items-center gap-2"><i class="fa-solid fa-receipt text-slate-400"></i> Tipo de Impuesto</label>
                    <input type="hidden" id="tipo_impuesto" value="ISR">
                    <div class="grid grid-cols-2 gap-4">
                        <button type="button" id="btn-impuesto-isr" onclick="seleccionarTipoImpuesto('ISR')" class="py-3 rounded-2xl font-bold border-2 border-brand-primary bg-brand-primary/10 text-brand-primary transition-all">
                            ISR
                        </button>
                        <button type="button" id="btn-impuesto-iva" onclick="seleccionarTipoImpuesto('IVA')" class="py-3 rounded-2xl font-bold border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all">
                            IVA
                        </button>
                    </div>
                </div>

                <!-- Monto Base & Porcentaje -->
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="label-base flex items-center gap-1.5"><i class="fa-solid fa-dollar-sign text-slate-400"></i> Monto Base</label>
                        <input type="number" step="0.01" id="monto_base" required class="input-base font-medium" placeholder="0.00">
                    </div>
                    <div>
                        <label class="label-base flex items-center gap-1.5"><i class="fa-solid fa-percent text-slate-400"></i> Porcentaje (%)</label>
                        <input type="number" step="0.01" id="porcentaje" required class="input-base font-medium" placeholder="Ej. 12.5" value="12.5">
                    </div>
                </div>

                <!-- Resumen Monto Retenido -->
                <div class="bg-brand-primary/5 rounded-2xl p-4 border border-brand-primary/20 flex justify-between items-center">
                    <span class="text-sm font-bold text-slate-700">Monto Retenido Calculado:</span>
                    <span id="monto_retenido_display" class="text-xl font-extrabold text-brand-primary">L 0.00</span>
                </div>

                <!-- Comentario / Observaciones -->
                <div>
                    <label class="label-base flex items-center gap-1.5"><i class="fa-solid fa-pen text-slate-400"></i> Comentario / Observaciones</label>
                    <textarea id="Comentario" rows="3" class="input-base resize-none" placeholder="Ej. Pago correspondiente a factura de servicios profesionales..."></textarea>
                </div>

                <!-- Botones Footer -->
                <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
                    <button type="button" onclick="closeModal('modal-retenciones')" class="btn-outline">Cerrar</button>
                    <button type="submit" class="btn-coral">
                        <i class="fa-solid fa-floppy-disk"></i> Registrar Retención
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- ================================================================= -->
    <!-- MODAL: NUEVO / EDITAR PROVEEDOR (COMO IMAGEN 1)                   -->
    <!-- ================================================================= -->
    <div id="modal-proveedores" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-xl relative animate-in fade-in zoom-in-95 duration-200">
            <!-- Botón Cerrar "X" -->
            <button type="button" onclick="closeModal('modal-proveedores')" class="absolute top-6 right-6 text-slate-400 hover:text-slate-600 text-xl font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-slate-100 transition-colors">
                <i class="fa-solid fa-xmark"></i>
            </button>

            <!-- Encabezado Modal -->
            <div class="flex items-center gap-3 mb-6">
                <div class="w-10 h-10 rounded-xl bg-brand-primary/10 text-brand-primary flex items-center justify-center text-lg">
                    <i class="fa-solid fa-user-plus"></i>
                </div>
                <h3 id="form-title-proveedores" class="text-2xl font-extrabold text-slate-800">Nuevo Proveedor</h3>
            </div>

            <form id="proveedorForm" class="space-y-5">
                <input type="hidden" id="prov_id">

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="label-base">RTN Proveedor</label>
                        <input type="text" id="prov_RTN_proveedor" required class="input-base" placeholder="0000-0000-000000" maxlength="14">
                    </div>
                    <div>
                        <label class="label-base">Nombre Comercial</label>
                        <input type="text" id="prov_proveedor" required class="input-base" placeholder="Nombre de la empresa">
                    </div>
                </div>

                <div>
                    <label class="label-base">Persona de Contacto</label>
                    <input type="text" id="prov_contacto" class="input-base" placeholder="Nombre del contacto principal">
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="label-base">Teléfono</label>
                        <input type="text" id="prov_telefono" class="input-base" placeholder="+504 0000-0000">
                    </div>
                    <div>
                        <label class="label-base">Correo Electrónico</label>
                        <input type="email" id="prov_correo" class="input-base" placeholder="ejemplo@correo.com">
                    </div>
                </div>

                <!-- Botones Footer -->
                <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
                    <button type="button" onclick="closeModal('modal-proveedores')" class="btn-outline">Cancelar</button>
                    <button type="submit" class="btn-coral">
                        <i class="fa-solid fa-floppy-disk"></i> Guardar
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL DOCUMENTOS CAI -->
    <div id="modal-documentos" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-xl relative">
            <button type="button" onclick="closeModal('modal-documentos')" class="absolute top-6 right-6 text-slate-400 hover:text-slate-600 text-xl font-bold"><i class="fa-solid fa-xmark"></i></button>
            <h3 class="text-2xl font-extrabold text-slate-800 mb-6 flex items-center gap-2"><i class="fa-solid fa-shield-halved text-brand-primary"></i> Registro de Autorización CAI</h3>
            <form id="documentoForm" class="space-y-4">
                <input type="hidden" id="doc_id">
                <div>
                    <label class="label-base">Clave CAI Autorizada</label>
                    <input type="text" id="doc_CAI" required class="input-base font-mono uppercase" placeholder="Ej: 48C542-CBC560-880DE0-63BE03-090937-71" maxlength="37">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="label-base">Prefijo</label>
                        <input type="text" id="doc_prefijo" required class="input-base font-mono" placeholder="Ej: 000-001-05">
                    </div>
                    <div>
                        <label class="label-base">Fecha Vencimiento</label>
                        <input type="date" id="doc_vence" required class="input-base">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-200">
                    <div>
                        <label class="label-base">Rango Inicial</label>
                        <input type="number" id="doc_serial_min" required class="input-base text-right font-mono" placeholder="1">
                    </div>
                    <div>
                        <label class="label-base">Rango Final</label>
                        <input type="number" id="doc_serial_max" required class="input-base text-right font-mono" placeholder="1000">
                    </div>
                </div>
                <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
                    <button type="button" onclick="closeModal('modal-documentos')" class="btn-outline">Cancelar</button>
                    <button type="submit" class="btn-coral">Guardar CAI</button>
                </div>
            </form>
        </div>
    </div>

    <!-- MODAL USUARIOS -->
    <div id="modal-usuarios" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md relative">
            <button type="button" onclick="closeModal('modal-usuarios')" class="absolute top-6 right-6 text-slate-400 hover:text-slate-600 text-xl font-bold"><i class="fa-solid fa-xmark"></i></button>
            <h3 class="text-2xl font-extrabold text-slate-800 mb-6 flex items-center gap-2"><i class="fa-solid fa-user-shield text-brand-primary"></i> Credenciales de Acceso</h3>
            <form id="usuarioForm" class="space-y-4">
                <input type="hidden" id="usu_id">
                <div>
                    <label class="label-base">Usuario</label>
                    <input type="text" id="usu_usuario" required class="input-base" placeholder="Ej: admin">
                </div>
                <div>
                    <label class="label-base">Nombre Completo</label>
                    <input type="text" id="usu_nombre" required class="input-base" placeholder="Ej: Breidy Funes">
                </div>
                <div>
                    <label class="label-base">Contraseña</label>
                    <input type="password" id="usu_clave" required class="input-base" placeholder="••••••••">
                </div>
                <div>
                    <label class="label-base">Rol</label>
                    <select id="usu_rol" class="input-base bg-white">
                        <option value="admin">Administrador</option>
                        <option value="usuario">Usuario</option>
                    </select>
                </div>
                <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
                    <button type="button" onclick="closeModal('modal-usuarios')" class="btn-outline">Cancelar</button>
                    <button type="submit" class="btn-coral">Guardar Usuario</button>
                </div>
            </form>
        </div>
    </div>

    <!-- TOAST & MODAL ERROR -->
    <div id="toast" class="fixed bottom-6 right-6 translate-y-[150%] transition-transform duration-300 z-50">
        <div class="bg-white text-slate-800 px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 border-l-4 border-brand-primary min-w-[300px]">
            <i class="fa-solid fa-circle-check text-brand-primary text-xl" id="toast-icon"></i>
            <p id="toast-msg" class="font-bold text-sm"></p>
        </div>
    </div>

    <div id="errorModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm hidden z-50 flex items-center justify-center">
        <div class="bg-white rounded-3xl shadow-2xl p-6 w-full max-w-sm text-center">
            <div class="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-4">
                <i class="fa-solid fa-triangle-exclamation text-3xl text-red-500"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-800 mb-2">Error de Validación</h3>
            <p id="errorMsg" class="text-slate-600 text-sm mb-6 px-4"></p>
            <button onclick="document.getElementById('errorModal').classList.add('hidden')" class="w-full btn-coral">Entendido</button>
        </div>
    </div>

    <script>
        let state = {
            retenciones: [
                { id: 1, fecha: "2026-01-27", proveedor_id: 24, documento_id: 1, num_documento: 502, monto_base: "25000.00", porcentaje: "12.5", monto_retenido: "3125.00", tipo_impuesto: "ISR", Num_factura: "000-001-04-00002351", CAI_factura: "3467F7-0254F3-A318E0-63BE03-09092D-C1", Fecha_factura: "2025-06-04", Comentario: "Datos Iniciales", estado: "ACTIVO" },
                { id: 2, fecha: "2026-01-27", proveedor_id: 24, documento_id: 1, num_documento: 503, monto_base: "25000.00", porcentaje: "12.5", monto_retenido: "3125.00", tipo_impuesto: "ISR", Num_factura: "000-001-04-00002366", CAI_factura: "3467F7-0254F3-A318E0-63BE03-09092D-C1", Fecha_factura: "2025-07-08", Comentario: "Datos Iniciales", estado: "ACTIVO" },
                { id: 3, fecha: "2026-02-16", proveedor_id: 13, documento_id: 1, num_documento: 504, monto_base: "4000.00", porcentaje: "12.5", monto_retenido: "500.00", tipo_impuesto: "ISR", Num_factura: "000-001-04-00000015", CAI_factura: "302C83-388C23-6C04E0-63BE03-090922-27", Fecha_factura: "2026-02-10", Comentario: "Datos Iniciales", estado: "ACTIVO" },
                { id: 4, fecha: "2026-02-16", proveedor_id: 13, documento_id: 1, num_documento: 505, monto_base: "18735.36", porcentaje: "12.5", monto_retenido: "2341.92", tipo_impuesto: "ISR", Num_factura: "000-001-04-00000014", CAI_factura: "302C83-388C23-6C04E0-63BE03-090922-27", Fecha_factura: "2026-02-10", Comentario: "Datos Iniciales", estado: "ACTIVO" },
                { id: 5, fecha: "2026-02-16", proveedor_id: 23, documento_id: 1, num_documento: 506, monto_base: "13440.00", porcentaje: "12.5", monto_retenido: "1680.00", tipo_impuesto: "ISR", Num_factura: "000-001-04-00000137", CAI_factura: "30B55E-B6AC51-0820E0-63BE03-090909-5D", Fecha_factura: "2026-02-10", Comentario: "Datos Iniciales", estado: "ACTIVO" }
            ],
            proveedores: [
                { id: 1, RTN_proveedor: "05011969021517", proveedor: "GERMAN EDGARDO LEITZELAR HERNANDEZ", contacto: "GERMAN EDGARDO LEITZELAR HERNANDEZ", telefono: "N/A", correo: "N/A" },
                { id: 2, RTN_proveedor: "08011999064243", proveedor: "LUIS FERNANDO FIGUEROA LOPEZ", contacto: "LUIS FERNANDO FIGUEROA LOPEZ", telefono: "N/A", correo: "N/A" },
                { id: 3, RTN_proveedor: "08011986130748", proveedor: "MAYBELL CRISTINA MEJIA AVILA", contacto: "MAYBELL CRISTINA MEJIA AVILA", telefono: "N/A", correo: "N/A" },
                { id: 4, RTN_proveedor: "08011989266721", proveedor: "ELIETH ALEJANDRA OCHOA MATAMOROS", contacto: "ELIETH ALEJANDRA OCHOA MATAMOROS", telefono: "N/A", correo: "N/A" },
                { id: 5, RTN_proveedor: "08011988159850", proveedor: "ANGELICA ABELINA ROMERO MARTINEZ", contacto: "ANGELICA ABELINA ROMERO MARTINEZ", telefono: "N/A", correo: "N/A" },
                { id: 6, RTN_proveedor: "07081987000695", proveedor: "MARIA BEATRIZ RODRIGUEZ MORAZAN", contacto: "MARIA BEATRIZ RODRIGUEZ MORAZAN", telefono: "N/A", correo: "N/A" },
                { id: 7, RTN_proveedor: "10072000004846", proveedor: "AUDELY ORELLANA YANEZ", contacto: "AUDELY ORELLANA YANEZ", telefono: "N/A", correo: "N/A" },
                { id: 8, RTN_proveedor: "08011982085409", proveedor: "AUDREY LENINA CRUZ ZELAYA", contacto: "AUDREY LENINA CRUZ ZELAYA", telefono: "N/A", correo: "N/A" },
                { id: 9, RTN_proveedor: "08011994012992", proveedor: "TANIA GABRIELA ACOSTA MARTINEZ", contacto: "TANIA GABRIELA ACOSTA MARTINEZ", telefono: "N/A", correo: "N/A" },
                { id: 10, RTN_proveedor: "08011999116642", proveedor: "ALEJANDRA CLARISA DOMINGUEZ JIMENEZ", contacto: "ALEJANDRA CLARISA DOMINGUEZ JIMENEZ", telefono: "N/A", correo: "N/A" },
                { id: 11, RTN_proveedor: "08011989088283", proveedor: "DARLING MICHELL ANDINO HERNANDEZ", contacto: "DARLING MICHELL ANDINO HERNANDEZ", telefono: "N/A", correo: "N/A" },
                { id: 12, RTN_proveedor: "08011994220546", proveedor: "JAAN BLADIMIR VALERIO CORRALES", contacto: "JAAN BLADIMIR VALERIO CORRALES", telefono: "N/A", correo: "N/A" },
                { id: 13, RTN_proveedor: "08012003199106", proveedor: "ANDREA ABIGAIL CASTRO CERRATO", contacto: "ANDREA ABIGAIL CASTRO CERRATO", telefono: "N/A", correo: "N/A" },
                { id: 14, RTN_proveedor: "08012001144665", proveedor: "JENNEVY SOHAM OSORIO SUAZO", contacto: "JENNEVY SOHAM OSORIO SUAZO", telefono: "N/A", correo: "N/A" },
                { id: 15, RTN_proveedor: "08261988002790", proveedor: "MARIA DEL ROSARIO VELASQUEZ ORTIZ", contacto: "MARIA DEL ROSARIO VELASQUEZ ORTIZ", telefono: "N/A", correo: "N/A" },
                { id: 16, RTN_proveedor: "08011995087742", proveedor: "RUT ALBERTINA LOBO CARDENAS", contacto: "RUT ALBERTINA LOBO CARDENAS", telefono: "N/A", correo: "N/A" },
                { id: 17, RTN_proveedor: "08012003075089", proveedor: "CESAR DANIEL CHAVARRIA GALEANO", contacto: "CESAR DANIEL CHAVARRIA GALEANO", telefono: "N/A", correo: "N/A" },
                { id: 18, RTN_proveedor: "07071999001116", proveedor: "KATHIA MARCELA MAYEN RAMIREZ", contacto: "KATHIA MARCELA MAYEN RAMIREZ", telefono: "N/A", correo: "N/A" },
                { id: 19, RTN_proveedor: "08011996053244", proveedor: "GRACIELA MARIA GARCIA VALLADARES", contacto: "GRACIELA MARIA GARCIA VALLADARES", telefono: "N/A", correo: "N/A" },
                { id: 20, RTN_proveedor: "08011962017735", proveedor: "OMAR ELIAS MEJIA ZUNIGA", contacto: "OMAR ELIAS MEJIA ZUNIGA", telefono: "N/A", correo: "N/A" },
                { id: 21, RTN_proveedor: "14131995000491", proveedor: "EDWIN OSMAR CHINCHILLA CASTILLO", contacto: "EDWIN OSMAR CHINCHILLA CASTILLO", telefono: "N/A", correo: "N/A" },
                { id: 22, RTN_proveedor: "08091995005733", proveedor: "ALBA RUT ENAMORADO ALMENDAREZ", contacto: "ALBA RUT ENAMORADO ALMENDAREZ", telefono: "N/A", correo: "N/A" },
                { id: 23, RTN_proveedor: "08011999113064", proveedor: "SHELCY REXCELL SERRANO BORJAS", contacto: "SHELCY REXCELL SERRANO BORJAS", telefono: "N/A", correo: "N/A" },
                { id: 24, RTN_proveedor: "08011986195418", proveedor: "AIDA YISSEL HENRIQUEZ MEDINA", contacto: "AIDA YISSEL HENRIQUEZ MEDINA", telefono: "N/A", correo: "N/A" }
            ],
            documentos: [
                { id: 1, prefijo: "000-001-05", serial_min: 1, serial_max: 1000, CAI: "48C542-CBC560-880DE0-63BE03-090937-71", vence: "2026-12-31", num_documento: 562, creado_por: "BFunes" }
            ],
            empresa: [{ id: 1, empresa: "FUNDACION PARA EL NIÑO QUEMADO", Nombre: "FUNDACION PARA EL NIÑO QUEMADO", RTN: "08019008131281", direccion: "Colonia Nueva Suyapa, anillo periférico, contiguo a Hospital Maria", telefono: "+504 2271-3302" }],
            usuarios: [{ id: 1, usuario: "admin", nombre: "Administrador", clave: "123", rol: "admin" }]
        };

        let currentPageRetenciones = 1;
        const pageSizeRetenciones = 10;

        function renderAll() {
            renderTableRetenciones();
            renderTableProveedores();
            renderTableDocumentos();
            renderTableUsuarios();
            renderFormEmpresa();
            renderProveedorCombobox();
            evaluarCAIActivo();
        }

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('fecha').valueAsDate = new Date();
            renderAll();
            
            document.getElementById('filtroBusquedaGlobal').addEventListener('input', filtrarRetenciones);
            document.getElementById('monto_base').addEventListener('input', calcularRetencion);
            document.getElementById('porcentaje').addEventListener('input', calcularRetencion);

            document.getElementById('Num_factura').addEventListener('input', function() {
                const el = document.getElementById('cont-fac');
                el.textContent = `Caracteres: ${this.value.length} / 19`;
                el.className = this.value.length === 19 ? 'text-[11px] font-bold text-emerald-600 mt-1' : 'text-[11px] font-bold text-red-600 mt-1';
            });
            document.getElementById('CAI_factura').addEventListener('input', function() {
                const el = document.getElementById('cont-cai');
                el.textContent = `Caracteres: ${this.value.length} / 37`;
                el.className = this.value.length === 37 ? 'text-[11px] font-bold text-emerald-600 mt-1' : 'text-[11px] font-bold text-red-600 mt-1';
            });

            document.getElementById('fecha').addEventListener('change', evaluarCAIActivo);
            setupProveedorCombobox();

            document.getElementById('retencionForm').addEventListener('submit', handleFormSubmitRetencion);
            document.getElementById('proveedorForm').addEventListener('submit', handleFormSubmitProveedor);
            document.getElementById('documentoForm').addEventListener('submit', handleFormSubmitDocumento);
            document.getElementById('usuarioForm').addEventListener('submit', handleFormSubmitUsuario);
            document.getElementById('empresaForm').addEventListener('submit', handleFormSubmitEmpresa);

            document.getElementById('searchRTNProv').addEventListener('input', filtrarProveedores);
        });

        function switchView(viewId) {
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.add('hidden'));
            document.getElementById(viewId).classList.remove('hidden');
            
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
            const activeNav = document.getElementById('nav-' + viewId);
            if (activeNav) activeNav.classList.add('active');
        }

        function abrirModal(modalId) {
            document.getElementById(modalId).classList.remove('hidden');
        }

        function closeModal(modalId) {
            document.getElementById(modalId).classList.add('hidden');
        }

        function seleccionarTipoImpuesto(tipo) {
            document.getElementById('tipo_impuesto').value = tipo;
            const btnIsr = document.getElementById('btn-impuesto-isr');
            const btnIva = document.getElementById('btn-impuesto-iva');
            if (tipo === 'ISR') {
                btnIsr.className = "py-3 rounded-2xl font-bold border-2 border-brand-primary bg-brand-primary/10 text-brand-primary transition-all";
                btnIva.className = "py-3 rounded-2xl font-bold border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all";
                document.getElementById('porcentaje').value = 12.5;
            } else {
                btnIva.className = "py-3 rounded-2xl font-bold border-2 border-brand-primary bg-brand-primary/10 text-brand-primary transition-all";
                btnIsr.className = "py-3 rounded-2xl font-bold border border-slate-200 bg-white text-slate-600 hover:bg-slate-50 transition-all";
                document.getElementById('porcentaje').value = 15;
            }
            calcularRetencion();
        }

        function abrirModalRetencion() {
            document.getElementById('retencionForm').reset();
            document.getElementById('retencion_id').value = '';
            document.getElementById('fecha').valueAsDate = new Date();
            document.getElementById('form-title-retenciones').textContent = "Nueva Retención";
            evaluarCAIActivo();
            abrirModal('modal-retenciones');
        }

        function abrirModalProveedor() {
            document.getElementById('proveedorForm').reset();
            document.getElementById('prov_id').value = '';
            document.getElementById('form-title-proveedores').textContent = "Nuevo Proveedor";
            abrirModal('modal-proveedores');
        }

        function abrirModalDocumento() {
            document.getElementById('documentoForm').reset();
            document.getElementById('doc_id').value = '';
            abrirModal('modal-documentos');
        }

        function abrirModalUsuario() {
            document.getElementById('usuarioForm').reset();
            document.getElementById('usu_id').value = '';
            abrirModal('modal-usuarios');
        }

        function calcularRetencion() {
            const base = parseFloat(document.getElementById('monto_base').value) || 0;
            const porcentaje = parseFloat(document.getElementById('porcentaje').value) || 0;
            const retenido = (base * porcentaje) / 100;
            document.getElementById('monto_retenido_display').textContent = `L ${retenido.toLocaleString('es-HN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        }

        function showToast(msg, type = 'success') {
            const toast = document.getElementById('toast');
            document.getElementById('toast-msg').textContent = msg;
            toast.classList.remove('translate-y-[150%]');
            setTimeout(() => toast.classList.add('translate-y-[150%]'), 3000);
        }

        function showError(msg) {
            document.getElementById('errorMsg').textContent = msg;
            document.getElementById('errorModal').classList.remove('hidden');
        }

        function renderAll() {
            renderTableRetenciones();
            renderTableProveedores();
            renderTableDocumentos();
            renderTableUsuarios();
            renderFormEmpresa();
            renderProveedorCombobox();
            evaluarCAIActivo();
        }

        function renderFormEmpresa() {
            if (state.empresa && state.empresa.length > 0) {
                const emp = state.empresa[0];
                if (document.getElementById('emp_id')) document.getElementById('emp_id').value = emp.id || 1;
                if (document.getElementById('emp_RTN')) document.getElementById('emp_RTN').value = emp.RTN || '';
                if (document.getElementById('emp_empresa')) document.getElementById('emp_empresa').value = emp.empresa || emp.Nombre || '';
                if (document.getElementById('emp_direccion')) document.getElementById('emp_direccion').value = emp.direccion || '';
                if (document.getElementById('emp_telefono')) document.getElementById('emp_telefono').value = emp.telefono || '';
            }
        }

        function evaluarCAIActivo() {
            if (document.getElementById('retencion_id').value) {
                return;
            }
            const fechaIngresada = new Date(document.getElementById('fecha').value);
            if(isNaN(fechaIngresada.getTime())) return;

            documentoActivo = null;
            let ultimoNumero = 0;

            const documentosValidos = state.documentos.filter(d => {
                const fechaVence = new Date(d.vence);
                fechaVence.setHours(23,59,59,999);
                return fechaVence >= fechaIngresada && (d.num_documento || 0) < d.serial_max;
            });

            if (documentosValidos.length > 0) {
                documentoActivo = documentosValidos[0];
                ultimoNumero = documentoActivo.num_documento || (documentoActivo.serial_min - 1);
                siguienteNumeroDoc = parseInt(ultimoNumero) + 1;
            }

            const alertBox = document.getElementById('cai_alert');
            const displayNum = document.getElementById('num_doc_display');
            const displayCai = document.getElementById('cai_display');
            const displayRango = document.getElementById('rango_display');

            if (documentoActivo) {
                alertBox.className = 'bg-brand-yellowBg text-brand-yellowText rounded-2xl p-5 mb-6 shadow-sm border border-amber-200/60 relative';
                displayNum.textContent = String(siguienteNumeroDoc).padStart(3, '0');
                displayCai.textContent = documentoActivo.CAI;
                displayRango.textContent = `${documentoActivo.serial_min} - ${documentoActivo.serial_max}`;
                document.getElementById('documento_id').value = documentoActivo.id;
                document.getElementById('num_documento_oculto').value = siguienteNumeroDoc;
            } else {
                alertBox.className = 'bg-red-50 text-red-700 rounded-2xl p-5 mb-6 shadow-sm border border-red-200 relative';
                displayNum.textContent = 'BLOQUEADO';
                displayCai.textContent = 'NO HAY CAI VIGENTE';
                displayRango.textContent = 'N/A';
                document.getElementById('documento_id').value = '';
                document.getElementById('num_documento_oculto').value = '';
            }
        }

        function renderTableRetenciones() {
            const tbody = document.getElementById('tabla-retenciones');
            const emptyState = document.getElementById('empty-state');
            tbody.innerHTML = '';
            let totalRetenidoSum = 0;
            
            if (state.retenciones.length === 0) {
                emptyState.classList.remove('hidden');
                tbody.parentNode.classList.add('hidden');
                document.getElementById('total-retenido-summary').textContent = 'L 0.00';
                return;
            }
            emptyState.classList.add('hidden');
            tbody.parentNode.classList.remove('hidden');

            state.retenciones.forEach(ret => {
                const prov = state.proveedores.find(p => p.id == ret.proveedor_id);
                const provName = prov ? prov.proveedor : 'Desconocido';
                const provRtn = prov ? prov.RTN_proveedor : '';
                const doc = state.documentos.find(d => d.id == ret.documento_id);
                const docPrefix = doc ? (doc.prefijo || doc.EPT || '') : 'N/A';
                const docStr = `${docPrefix}-${String(ret.num_documento).padStart(8, '0')}`;
                const montoRet = parseFloat(ret.monto_retenido) || 0;

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-amber-50/40 transition-colors border-b border-slate-100/70 text-sm';
                tr.dataset.searchable = `${docStr} ${provName} ${provRtn} ${ret.Num_factura}`.toLowerCase();

                tr.innerHTML = `
                    <td class="py-4 px-6">
                        <div class="badge-yellow mb-1">${docStr}</div>
                        <div><span class="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-100 text-emerald-800">${ret.estado}</span></div>
                    </td>
                    <td class="py-4 px-6 text-slate-600 font-medium text-xs">${ret.fecha}</td>
                    <td class="py-4 px-6">
                        <div class="font-extrabold text-slate-800 text-sm">${provName}</div>
                        <div class="badge-yellow text-[10px] mt-0.5 font-mono">${provRtn}</div>
                    </td>
                    <td class="py-4 px-6 text-right font-extrabold text-brand-primary text-base">L ${montoRet.toLocaleString('es-HN', { minimumFractionDigits: 2 })}</td>
                    <td class="py-4 px-6 text-center">
                        <div class="flex items-center justify-center gap-1.5">
                            <button onclick="showToast('Generando vista de impresión...')" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-print text-xs"></i></button>
                            <button onclick="editarRetencion(${ret.id})" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-pen text-xs"></i></button>
                            <button onclick="cambiarEstadoRetencion(${ret.id}, 'ANULADO')" class="w-8 h-8 rounded-xl bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-xmark text-xs"></i></button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById('total-retenido-summary').textContent = `L ${totalRetenidoSum.toLocaleString('es-HN', { minimumFractionDigits: 2 })}`;
        }

        function renderTableProveedores() {
            const tbody = document.getElementById('tabla-proveedores');
            tbody.innerHTML = '';
            state.proveedores.forEach(p => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-slate-100 hover:bg-amber-50/40 text-sm transition-colors';
                tr.dataset.rtn = (p.RTN_proveedor || '').toLowerCase();
                tr.dataset.nombre = (p.proveedor || '').toLowerCase();
                tr.innerHTML = `
                    <td class="py-4 px-6 font-extrabold text-slate-800">${p.proveedor}</td>
                    <td class="py-4 px-6"><span class="badge-yellow font-mono text-xs">${p.RTN_proveedor}</span></td>
                    <td class="py-4 px-6 text-xs text-slate-600 font-medium">${p.contacto || p.proveedor}</td>
                    <td class="py-4 px-6 text-xs text-slate-500 space-y-0.5">
                        <div class="flex items-center gap-1.5"><i class="fa-solid fa-phone text-slate-400 text-[10px]"></i> ${p.telefono || 'N/A'}</div>
                        <div class="flex items-center gap-1.5"><i class="fa-regular fa-envelope text-slate-400 text-[10px]"></i> ${p.correo || 'N/A'}</div>
                    </td>
                    <td class="py-4 px-6 text-center">
                        <div class="flex items-center justify-center gap-1.5">
                            <button onclick="showToast('Consultando proveedor...')" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all flex items-center justify-center"><i class="fa-solid fa-id-card text-xs"></i></button>
                            <button onclick="editarProveedor(${p.id})" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all flex items-center justify-center"><i class="fa-solid fa-pen text-xs"></i></button>
                            <button onclick="showToast('Función deshabilitada para registros activos')" class="w-8 h-8 rounded-xl bg-slate-100 text-slate-400 flex items-center justify-center"><i class="fa-solid fa-trash-can text-xs"></i></button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderTableDocumentos() {
            const tbody = document.getElementById('tabla-documentos');
            tbody.innerHTML = '';
            state.documentos.forEach(d => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-slate-100 hover:bg-amber-50/40 text-sm transition-colors';
                tr.innerHTML = `
                    <td class="py-4 px-6 font-extrabold text-slate-800"><span class="badge-yellow font-mono">${d.prefijo || d.EPT}</span></td>
                    <td class="py-4 px-6 font-mono text-xs">${d.serial_min} al ${d.serial_max}</td>
                    <td class="py-4 px-6 font-mono text-xs text-slate-600">${d.CAI}</td>
                    <td class="py-4 px-6 text-xs text-slate-600 font-medium">${d.vence}</td>
                    <td class="py-4 px-6 text-center font-extrabold text-brand-primary text-base">${d.num_documento || 0}</td>
                    <td class="py-4 px-6 text-center">
                        <button onclick="editarDocumento(${d.id})" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all inline-flex items-center justify-center"><i class="fa-solid fa-pen text-xs"></i></button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderTableUsuarios() {
            const tbody = document.getElementById('tabla-usuarios');
            tbody.innerHTML = '';
            state.usuarios.forEach(u => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-slate-100 hover:bg-amber-50/40 text-sm transition-colors';
                tr.innerHTML = `
                    <td class="py-4 px-6 text-slate-400 font-bold">${u.id}</td>
                    <td class="py-4 px-6 font-extrabold text-slate-800">${u.usuario}</td>
                    <td class="py-4 px-6 text-slate-600 text-xs font-medium">${u.nombre || u.usuario}</td>
                    <td class="py-4 px-6 text-center"><span class="px-3 py-1 rounded-full text-[10px] font-extrabold bg-slate-100 text-slate-700 uppercase tracking-wider">${u.rol || 'usuario'}</span></td>
                    <td class="py-4 px-6 text-center">
                        <button onclick="editarUsuario(${u.id})" class="w-8 h-8 rounded-xl bg-orange-50 text-brand-primary hover:bg-brand-primary hover:text-white transition-all inline-flex items-center justify-center"><i class="fa-solid fa-pen text-xs"></i></button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function setupProveedorCombobox() {
            const searchInput = document.getElementById('proveedor_search');
            const dropdown = document.getElementById('proveedor_dropdown');
            const icon = document.getElementById('proveedor_icon');

            searchInput.addEventListener('focus', () => {
                dropdown.classList.remove('hidden');
                if(icon) icon.classList.add('rotate-180');
                filtrarCombobox();
            });

            searchInput.addEventListener('blur', () => {
                setTimeout(() => {
                    dropdown.classList.add('hidden');
                    if(icon) icon.classList.remove('rotate-180');
                    validarSeleccionCombobox();
                }, 200);
            });

            searchInput.addEventListener('input', filtrarCombobox);
        }

        function renderProveedorCombobox() {
            const ul = document.getElementById('proveedor_list');
            ul.innerHTML = '';
            state.proveedores.forEach(p => {
                const li = document.createElement('li');
                li.className = 'px-4 py-2.5 hover:bg-amber-50 cursor-pointer border-b border-slate-50 flex justify-between items-center transition-colors';
                li.dataset.id = p.id;
                li.dataset.search = `${p.proveedor} ${p.RTN_proveedor}`.toLowerCase();
                li.innerHTML = `
                    <div>
                        <div class="font-bold text-slate-800 text-xs">${p.proveedor}</div>
                        <div class="text-[10px] text-amber-700 font-mono">${p.RTN_proveedor}</div>
                    </div>
                    <i class="fa-solid fa-check text-xs text-brand-primary opacity-0"></i>
                `;
                li.onmousedown = () => seleccionarProveedor(p.id, p.proveedor);
                ul.appendChild(li);
            });
        }

        function filtrarCombobox() {
            const filter = document.getElementById('proveedor_search').value.toLowerCase();
            const items = document.getElementById('proveedor_list').querySelectorAll('li');
            items.forEach(item => {
                if (item.dataset.search.includes(filter)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function seleccionarProveedor(id, nombre) {
            document.getElementById('proveedor_id').value = id;
            document.getElementById('proveedor_search').value = nombre;
            document.getElementById('proveedor_dropdown').classList.add('hidden');
        }

        function validarSeleccionCombobox() {
            const currentId = document.getElementById('proveedor_id').value;
            if (!currentId) {
                document.getElementById('proveedor_search').value = '';
            }
        }

        function handleFormSubmitRetencion(e) {
            e.preventDefault();
            if(document.getElementById('Num_factura').value.length !== 19) {
                showError("El número de factura debe tener exactamente 19 caracteres.");
                return;
            }
            if(document.getElementById('CAI_factura').value.length !== 37) {
                showError("El CAI de la factura debe tener exactamente 37 caracteres.");
                return;
            }
            
            const id = document.getElementById('retencion_id').value;
            const reg = {
                id: id ? parseInt(id) : state.retenciones.length + 1,
                fecha: document.getElementById('fecha').value,
                proveedor_id: parseInt(document.getElementById('proveedor_id').value),
                documento_id: parseInt(document.getElementById('documento_id').value),
                num_documento: parseInt(document.getElementById('num_documento_oculto').value),
                monto_base: document.getElementById('monto_base').value,
                porcentaje: document.getElementById('porcentaje').value,
                monto_retenido: ((parseFloat(document.getElementById('monto_base').value) * parseFloat(document.getElementById('porcentaje').value)) / 100).toFixed(2),
                tipo_impuesto: document.getElementById('tipo_impuesto').value,
                Num_factura: document.getElementById('Num_factura').value,
                CAI_factura: document.getElementById('CAI_factura').value,
                Fecha_factura: document.getElementById('Fecha_factura').value,
                Comentario: document.getElementById('Comentario').value,
                estado: "ACTIVO"
            };

            if(id) {
                const idx = state.retenciones.findIndex(r => r.id == id);
                if(idx > -1) {
                    reg.num_documento = state.retenciones[idx].num_documento;
                    reg.documento_id = state.retenciones[idx].documento_id;
                    state.retenciones[idx] = reg;
                }
            } else {
                state.retenciones.unshift(reg);
            }

            renderTableRetenciones();
            closeModal('modal-retenciones');
            showToast("Comprobante guardado correctamente", "success");
        }

        function handleFormSubmitProveedor(e) {
            e.preventDefault();
            const id = document.getElementById('prov_id').value;
            const p = {
                id: id ? parseInt(id) : state.proveedores.length + 1,
                RTN_proveedor: document.getElementById('prov_RTN_proveedor').value,
                proveedor: document.getElementById('prov_proveedor').value,
                contacto: document.getElementById('prov_contacto').value,
                telefono: document.getElementById('prov_telefono').value,
                correo: document.getElementById('prov_correo').value
            };
            if(id) {
                const idx = state.proveedores.findIndex(item => item.id == id);
                if(idx > -1) state.proveedores[idx] = p;
            } else {
                state.proveedores.unshift(p);
            }
            renderTableProveedores();
            renderProveedorCombobox();
            closeModal('modal-proveedores');
            showToast("Proveedor guardado correctamente", "success");
        }

        function handleFormSubmitDocumento(e) {
            e.preventDefault();
            const id = document.getElementById('doc_id').value;
            const d = {
                id: id ? parseInt(id) : state.documentos.length + 1,
                CAI: document.getElementById('doc_CAI').value,
                prefijo: document.getElementById('doc_prefijo').value,
                vence: document.getElementById('doc_vence').value,
                serial_min: parseInt(document.getElementById('doc_serial_min').value),
                serial_max: parseInt(document.getElementById('doc_serial_max').value),
                num_documento: 0
            };
            if(id) {
                const idx = state.documentos.findIndex(item => item.id == id);
                if(idx > -1) state.documentos[idx] = d;
            } else {
                state.documentos.unshift(d);
            }
            renderTableDocumentos();
            evaluarCAIActivo();
            closeModal('modal-documentos');
            showToast("Autorización CAI guardada", "success");
        }

        function handleFormSubmitUsuario(e) {
            e.preventDefault();
            const id = document.getElementById('usu_id').value;
            const u = {
                id: id ? parseInt(id) : state.usuarios.length + 1,
                usuario: document.getElementById('usu_usuario').value,
                nombre: document.getElementById('usu_nombre').value,
                clave: document.getElementById('usu_clave').value,
                rol: document.getElementById('usu_rol').value
            };
            if(id) {
                const idx = state.usuarios.findIndex(item => item.id == id);
                if(idx > -1) state.usuarios[idx] = u;
            } else {
                state.usuarios.unshift(u);
            }
            renderTableUsuarios();
            closeModal('modal-usuarios');
            showToast("Usuario guardado", "success");
        }

        function handleFormSubmitEmpresa(e) {
            e.preventDefault();
            state.empresa[0] = {
                id: 1,
                RTN: document.getElementById('emp_RTN').value,
                empresa: document.getElementById('emp_empresa').value,
                direccion: document.getElementById('emp_direccion').value,
                telefono: document.getElementById('emp_telefono').value
            };
            showToast("Datos de la empresa actualizados", "success");
        }

        function editarRetencion(id) {
            const ret = state.retenciones.find(r => r.id === id);
            if(!ret) return;
            document.getElementById('retencion_id').value = ret.id;
            document.getElementById('documento_id').value = ret.documento_id;
            document.getElementById('num_documento_oculto').value = ret.num_documento;

            const alertBox = document.getElementById('cai_alert');
            const displayNum = document.getElementById('num_doc_display');
            const displayCai = document.getElementById('cai_display');
            const displayRango = document.getElementById('rango_display');
            
            const doc = state.documentos.find(d => d.id == ret.documento_id) || (state.documentos[0] || {});
            alertBox.className = 'bg-brand-yellowBg text-brand-yellowText rounded-2xl p-5 mb-6 shadow-sm border border-amber-200/60 relative';
            displayNum.textContent = String(ret.num_documento).padStart(3, '0');
            displayCai.textContent = doc.CAI || 'N/A';
            displayRango.textContent = doc.serial_min ? `${doc.serial_min} - ${doc.serial_max}` : 'N/A';

            document.getElementById('fecha').value = ret.fecha || '';
            seleccionarProveedor(ret.proveedor_id, state.proveedores.find(p => p.id == ret.proveedor_id)?.proveedor || '');
            document.getElementById('Num_factura').value = ret.Num_factura;
            document.getElementById('CAI_factura').value = ret.CAI_factura;
            document.getElementById('Fecha_factura').value = ret.Fecha_factura || '';
            document.getElementById('monto_base').value = ret.monto_base;
            document.getElementById('porcentaje').value = ret.porcentaje;
            document.getElementById('Comentario').value = ret.Comentario || '';
            seleccionarTipoImpuesto(ret.tipo_impuesto || 'ISR');
            document.getElementById('form-title-retenciones').textContent = "Editar Retención";
            abrirModal('modal-retenciones');
        }

        function editarProveedor(id) {
            const p = state.proveedores.find(item => item.id === id);
            if(!p) return;
            document.getElementById('prov_id').value = p.id;
            document.getElementById('prov_RTN_proveedor').value = p.RTN_proveedor;
            document.getElementById('prov_proveedor').value = p.proveedor;
            document.getElementById('prov_contacto').value = p.contacto || '';
            document.getElementById('prov_telefono').value = p.telefono || '';
            document.getElementById('prov_correo').value = p.correo || '';
            document.getElementById('form-title-proveedores').textContent = "Editar Proveedor";
            abrirModal('modal-proveedores');
        }

        function editarDocumento(id) {
            const d = state.documentos.find(item => item.id === id);
            if(!d) return;
            document.getElementById('doc_id').value = d.id;
            document.getElementById('doc_CAI').value = d.CAI;
            document.getElementById('doc_prefijo').value = d.prefijo || d.EPT;
            document.getElementById('doc_vence').value = d.vence;
            document.getElementById('doc_serial_min').value = d.serial_min;
            document.getElementById('doc_serial_max').value = d.serial_max;
            abrirModal('modal-documentos');
        }

        function editarUsuario(id) {
            const u = state.usuarios.find(item => item.id === id);
            if(!u) return;
            document.getElementById('usu_id').value = u.id;
            document.getElementById('usu_usuario').value = u.usuario;
            document.getElementById('usu_nombre').value = u.nombre || '';
            document.getElementById('usu_clave').value = u.clave;
            document.getElementById('usu_rol').value = u.rol || 'usuario';
            abrirModal('modal-usuarios');
        }

        function cambiarEstadoRetencion(id, estado) {
            const ret = state.retenciones.find(r => r.id === id);
            if(ret) {
                ret.estado = estado;
                renderTableRetenciones();
                showToast(`Retención marcada como ${estado}`);
            }
        }

        function filtrarRetenciones() {
            const query = document.getElementById('filtroBusquedaGlobal').value.toLowerCase();
            document.querySelectorAll('#tabla-retenciones tr').forEach(row => {
                const match = (row.dataset.searchable || '').includes(query);
                row.style.display = match ? '' : 'none';
            });
        }

        function filtrarProveedores() {
            const filter = document.getElementById('searchRTNProv').value.toLowerCase();
            document.querySelectorAll('#tabla-proveedores tr').forEach(row => {
                const match = (row.dataset.rtn || '').includes(filter) || (row.dataset.nombre || '').includes(filter);
                row.style.display = match ? '' : 'none';
            });
        }
    </script>
</body>
</html>'''

target_path = r'd:\AppScript\retenciones\frontend.html'
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully wrote {len(html_content)} bytes to {target_path}")
