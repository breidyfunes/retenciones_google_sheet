const SHEET_RETENCIONES = "retenciones";
const SHEET_PROVEEDORES = "proveedores";
const SHEET_DOCUMENTOS = "documentos";
const SHEET_EMPRESA = "empresa";
const SHEET_USUARIOS = "usuarios";

/**
 * Crea un menú personalizado en la interfaz de Google Sheets al abrir el archivo.
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('⚙️ Sistema Fiscal')
    .addItem('🚀 Inicializar / Verificar Hojas y Columnas', 'inicializarTodasLasHojas')
    .addToUi();
}

/**
 * Función principal doGet: Sirve el HTML o responde peticiones API JSON.
 */
function doGet(e) {
  try {
    const action = e && e.parameter && e.parameter.action;
    
    // Si viene con un parámetro de acción, actúa como API y devuelve JSON
    if (action === "all") {
      const data = getInitialData();
      return ContentService.createTextOutput(JSON.stringify({ status: "success", data: data }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    // Si se accede sin parámetros, sirve la interfaz gráfica HTML
    return HtmlService.createHtmlOutputFromFile('index')
      .setTitle('Sistema de Retenciones - Gestión Fiscal SAR')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Maneja las peticiones POST (Guardar o actualizar registros desde API externa)
 */
function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const tabla = payload.tabla;
    const registro = payload.registro;
    
    const result = saveRegistro(tabla, registro);
    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Obtiene todos los datos iniciales de la hoja de cálculo.
 * Invocable directamente mediante google.script.run desde el Frontend.
 */
function getInitialData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  return {
    retenciones: getDataFromSheet(ss, SHEET_RETENCIONES),
    proveedores: getDataFromSheet(ss, SHEET_PROVEEDORES),
    documentos: getDataFromSheet(ss, SHEET_DOCUMENTOS),
    empresa: getDataFromSheet(ss, SHEET_EMPRESA),
    usuarios: getDataFromSheet(ss, SHEET_USUARIOS)
  };
}

/**
 * Función centralizada para guardar o actualizar un registro en cualquier tabla.
 * Invocable tanto por google.script.run como por doPost.
 */
function saveRegistro(tabla, registro) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(tabla);
  
  if (!sheet) {
    return { status: "error", message: "Tabla no encontrada: " + tabla };
  }
  
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  
  // Seguridad: Hashing de contraseñas para la tabla usuarios
  if (tabla === SHEET_USUARIOS && registro.clave) {
    if (registro.clave.length !== 64) {
      registro.clave = hashPassword(registro.clave);
    }
  }

  if (tabla === SHEET_PROVEEDORES) {
    if (registro.RTN_proveedor !== undefined && registro.RTN_proveedor !== null) {
      let rtnStr = String(registro.RTN_proveedor).trim();
      if (rtnStr.startsWith("'")) {
        rtnStr = rtnStr.substring(1);
      }
      if (rtnStr.length === 13) {
        rtnStr = "0" + rtnStr;
      }
      registro.RTN_proveedor = rtnStr;
    }
    if (registro.telefono !== undefined && registro.telefono !== null) {
      let telStr = String(registro.telefono).trim();
      if (telStr.startsWith("'")) {
        telStr = telStr.substring(1);
      }
      registro.telefono = telStr;
    }
  }

  // Normalización del tipo de impuesto (ISR / ISV)
  if (tabla === SHEET_RETENCIONES && registro.tipo_impuesto) {
    if (registro.tipo_impuesto === 'IVA') registro.tipo_impuesto = 'ISV';
    if (registro.tipo_impuesto === 'IRS') registro.tipo_impuesto = 'ISR';
  }

  let savedId = registro.id;

  if (registro.id) {
    // Actualizar registro existente
    const rows = sheet.getDataRange().getValues();
    let rowIndex = -1;
    for (let i = 1; i < rows.length; i++) {
      if (rows[i][0] == registro.id) {
        rowIndex = i + 1;
        break;
      }
    }
    
    if (rowIndex > -1) {
      const targetRange = sheet.getRange(rowIndex, 1, 1, headers.length);
      if (tabla === SHEET_PROVEEDORES) {
        const rtnIdx = headers.indexOf('RTN_proveedor');
        const telIdx = headers.indexOf('telefono');
        if (rtnIdx !== -1) sheet.getRange(rowIndex, rtnIdx + 1).setNumberFormat("@");
        if (telIdx !== -1) sheet.getRange(rowIndex, telIdx + 1).setNumberFormat("@");
      }
      
      const rowData = headers.map(header => registro[header] !== undefined ? registro[header] : "");
      targetRange.setValues([rowData]);
    } else {
      return { status: "error", message: "Registro no encontrado para actualizar" };
    }
    
  } else {
    // Crear nuevo registro (Asignar ID automático)
    const lastRow = sheet.getLastRow();
    let newId = 1;
    if (lastRow > 1) {
      const ids = sheet.getRange(2, 1, lastRow - 1, 1).getValues().flat();
      newId = Math.max(...ids.filter(id => !isNaN(id) && id !== ""), 0) + 1;
    }
    registro.id = newId;
    savedId = newId;
    
    if (headers.includes('created_at') && !registro.created_at) {
      registro.created_at = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
    }
    
    const nextRow = sheet.getLastRow() + 1;
    
    if (tabla === SHEET_PROVEEDORES) {
      const rtnIdx = headers.indexOf('RTN_proveedor');
      const telIdx = headers.indexOf('telefono');
      if (rtnIdx !== -1) sheet.getRange(nextRow, rtnIdx + 1).setNumberFormat("@");
      if (telIdx !== -1) sheet.getRange(nextRow, telIdx + 1).setNumberFormat("@");
    }

    const rowData = headers.map(header => registro[header] !== undefined ? registro[header] : "");
    const targetRange = sheet.getRange(nextRow, 1, 1, rowData.length);
    targetRange.setValues([rowData]);

    // Lógica especial: Si es nueva retención, incrementar el correlativo del documento CAI correspondiente
    if (tabla === SHEET_RETENCIONES && registro.documento_id && registro.num_documento) {
      actualizarCorrelativoDocumento(ss, registro.documento_id, registro.num_documento);
    }
  }

  return { status: "success", id: savedId, registro: registro, data: getInitialData() };
}

/**
 * Incrementa el contador num_documento en la hoja de documentos CAI
 */
function actualizarCorrelativoDocumento(ss, documentoId, ultimoNumeroUsado) {
  const sheetDoc = ss.getSheetByName(SHEET_DOCUMENTOS);
  if (!sheetDoc) return;
  
  const rows = sheetDoc.getDataRange().getValues();
  const headers = rows[0];
  const idColIdx = 0;
  const numDocColIdx = headers.indexOf('num_documento');

  if (numDocColIdx === -1) return;

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][idColIdx] == documentoId) {
      sheetDoc.getRange(i + 1, numDocColIdx + 1).setValue(ultimoNumeroUsado);
      break;
    }
  }
}

/**
 * Cambia el estado de una retención (ej. ANULADO)
 */
function cambiarEstadoRetencion(id, nuevoEstado) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_RETENCIONES);
  if (!sheet) return { status: "error", message: "Tabla retenciones no encontrada" };

  const rows = sheet.getDataRange().getValues();
  const headers = rows[0];
  const estadoColIdx = headers.indexOf('estado');

  if (estadoColIdx === -1) return { status: "error", message: "Columna estado no existe" };

  for (let i = 1; i < rows.length; i++) {
    if (rows[i][0] == id) {
      sheet.getRange(i + 1, estadoColIdx + 1).setValue(nuevoEstado);
      return { status: "success", data: getInitialData() };
    }
  }
  return { status: "error", message: "Retención no encontrada" };
}

/**
 * Encripta una cadena utilizando el algoritmo SHA-256
 */
function hashPassword(text) {
  const rawHash = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, text, Utilities.Charset.UTF_8);
  let txtHash = "";
  for (let i = 0; i < rawHash.length; i++) {
    let byteVal = rawHash[i];
    if (byteVal < 0) byteVal += 256;
    let byteHex = byteVal.toString(16);
    if (byteHex.length === 1) byteHex = "0" + byteHex;
    txtHash += byteHex;
  }
  return txtHash;
}

/**
 * Extrae los datos de una hoja y los convierte en objetos JSON
 */
function getDataFromSheet(ss, sheetName) {
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
    inicializarEstructuraHoja(sheet, sheetName);
  }
  
  const range = sheet.getDataRange();
  const values = range.getValues();
  
  if (values.length <= 1) return [];
  
  const headers = values[0];
  const rows = values.slice(1);
  
  return rows.map(row => {
    let obj = {};
    headers.forEach((header, index) => {
      let val = row[index];
      if (val instanceof Date) {
        val = Utilities.formatDate(val, Session.getScriptTimeZone(), "yyyy-MM-dd");
      }
      
      // Garantizar que RTN_proveedor y teléfono se devuelvan como texto, sin comilla inicial y con cero preservado
      if (sheetName === SHEET_PROVEEDORES && (header === 'RTN_proveedor' || header === 'telefono')) {
        val = val !== null && val !== undefined ? String(val).trim() : "";
        if (val.startsWith("'")) {
          val = val.substring(1);
        }
        if (header === 'RTN_proveedor' && val.length === 13) {
          val = "0" + val;
        }
      }
      
      obj[header] = val;
    });
    return obj;
  });
}

/**
 * Inicializa los encabezados predeterminados para cada hoja
 */
function inicializarTodasLasHojas() {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const nombres = [SHEET_RETENCIONES, SHEET_PROVEEDORES, SHEET_DOCUMENTOS, SHEET_EMPRESA, SHEET_USUARIOS];
    
    nombres.forEach(nombre => {
      let sheet = ss.getSheetByName(nombre);
      if (!sheet) {
        sheet = ss.insertSheet(nombre);
      }
      if (sheet.getLastRow() === 0) {
        inicializarEstructuraHoja(sheet, nombre);
      }
    });
    
    SpreadsheetApp.getUi().alert('¡Éxito!', 'Todas las hojas y estructuras de columnas han sido verificadas e inicializadas correctamente.', SpreadsheetApp.getUi().ButtonSet.OK);
  } catch (error) {
    SpreadsheetApp.getUi().alert('Error', 'Ocurrió un error al inicializar: ' + error.toString(), SpreadsheetApp.getUi().ButtonSet.OK);
  }
}

function inicializarEstructuraHoja(sheet, sheetName) {
  let headers = [];
  
  switch(sheetName) {
    case SHEET_RETENCIONES:
      headers = ['id', 'fecha', 'proveedor_id', 'documento_id', 'num_documento', 'monto_base', 'porcentaje', 'monto_retenido', 'tipo_impuesto', 'created_at', 'creado_por', 'Num_factura', 'CAI_factura', 'Fecha_factura', 'Comentario', 'estado'];
      break;
    case SHEET_PROVEEDORES:
      headers = ['id', 'RTN_proveedor', 'proveedor', 'contacto', 'telefono', 'correo', 'created_at', 'creado_por'];
      sheet.getRange("B:B").setNumberFormat("@");
      sheet.getRange("E:E").setNumberFormat("@");
      break;
    case SHEET_DOCUMENTOS:
      headers = ['id', 'prefijo', 'serial_min', 'serial_max', 'CAI', 'vence', 'created_at', 'num_documento', 'creado_por'];
      sheet.appendRow(headers);
      sheet.appendRow([1, '000-001-05', 1, 1000, '48C542-CBC560-880DE0-63BE03-090937-71', '2026-12-31', '2026-05-10 22:40:53', 562, 'BFunes']);
      return;
    case SHEET_EMPRESA:
      headers = ['id', 'empresa', 'RTN', 'direccion', 'telefono', 'logotipo', 'created_at', 'creado_por'];
      sheet.appendRow(headers);
      sheet.appendRow([1, 'FUNDACION PARA EL NIÑO QUEMADO', '08019008131281', 'Colonia Nueva Suyapa, anillo periférico, contiguo a Hospital Maria', '+504 2271-3302', '', '2026-05-10 22:40:53', 'BFunes']);
      return;
    case SHEET_USUARIOS:
      headers = ['id', 'usuario', 'nombre', 'clave', 'created_at', 'rol'];
      sheet.appendRow(headers);
      sheet.appendRow([1, 'admin', 'Administrador', hashPassword('admin123'), '2026-05-10 22:40:53', 'admin']);
      return;
  }
  
  if (headers.length > 0) {
    sheet.appendRow(headers);
  }
}
