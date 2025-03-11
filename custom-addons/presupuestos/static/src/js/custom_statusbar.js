odoo.define('presupuestos.CustomStatusBar', function (require) {
    "use strict";

    var StatusBar = require('web.StatusBar');
    var field_registry = require('web.field_registry');

    var CustomStatusBar = StatusBar.extend({
        _render: function () {
            var self = this;
            var state = this.recordData.state; // Estado actual del registro
            var states_to_show = [];

            // Lista completa de estados posibles (definida en statusbar_visible o en el modelo)
            var all_states = this.statusbarValues || [];

            // Filtrar los estados que se mostrarán según el estado actual
            all_states.forEach(function (status) {
                var status_value = status[0]; // El valor del estado (ej. 'presupuesto_pedido')
                if (state === 'presupuesto_pedido' && status_value === 'presupuesto_servicio') {
                    return; // No agregar 'presupuesto_servicio' si estamos en 'presupuesto_pedido'
                } else if (state === 'presupuesto_servicio' && status_value === 'presupuesto_pedido') {
                    return; // No agregar 'presupuesto_pedido' si estamos en 'presupuesto_servicio'
                } else {
                    states_to_show.push(status); // Agregar el estado si no hay restricción
                }
            });

            // Actualizar los estados visibles en el widget
            this.statusbarValues = states_to_show;

            // Renderizar la barra de estado con los estados filtrados
            this._super.apply(this, arguments);
        },
    });

    field_registry.add('custom_statusbar', CustomStatusBar);
    return CustomStatusBar;
});