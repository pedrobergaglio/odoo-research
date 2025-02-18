/** @odoo-module */

import { Chatter } from "@mail/discuss/chatter/chatter";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(Chatter.prototype, 'hide_chatter.Chatter', {
    setup() {
        this._super(...arguments);
        this.orm = useService("orm");
        this._hideChatterIfNeeded();
    },

    async _hideChatterIfNeeded() {
        try {
            const configParam = await this.orm.call(
                "ir.config_parameter",
                "get_param",
                ["hide_chatter.model_ids"]
            );
            
            if (!configParam) return;
            
            // Parse the stored model IDs (stored as string)
            const modelIds = JSON.parse(configParam || '[]');
            
            // Get current model ID
            const currentModel = await this.orm.searchRead(
                "ir.model",
                [["model", "=", this.props.threadModel || this.props.resModel]],
                ["id"],
                { limit: 1 }
            );

            if (currentModel.length && modelIds.includes(currentModel[0].id)) {
                // Hide using both modern and legacy approaches
                if (this.el) {
                    this.el.style.display = 'none';
                }
                if (this.rootRef?.el) {
                    this.rootRef.el.style.display = 'none';
                }
                // Also try setting the visible prop if available
                if (this.props) {
                    this.props.isVisible = false;
                }
            }
        } catch (error) {
            console.error("Failed to check chatter visibility:", error);
        }
    }
});
