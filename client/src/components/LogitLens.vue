<template>
    <b-container fluid>
        <b-row>
            <b-tabs pills>
                <b-tab :title-item-class="logitlens_items.length == 1 ? 'd-none' : ''" v-for="logitlens_data in logitlens_items" :title="logitlens_data.name"
                    :key="'tab-logitlens-' + logitlens_data.name">
                    <b-tabs pills vertical class="mt-3" v-model="logitlens_tabs">
                        <b-tab :title-item-class="logitlens_data.data.length == 1 ? 'd-none' : ''" :title="_logitlens_data.name" v-for="_logitlens_data in logitlens_data.data"
                            :key="'tab-logitlens-' + logitlens_data.name + '-' + _logitlens_data.name">
                            <b-table head-row-variant="light" bordered sticky-header="100vh"
                                :items="_logitlens_data.data" :fields="_logitlens_data.fields" class="text-center">
                                <template #head()="data">
                                    <b-button v-if="'index' in data.field" @click="rewrite_token_index = data.field.index"
                                        :variant="rewrite_token_index == data.field.index ? 'warning' : 'outline-dark'"
                                        :disabled="!rewrite_toggle">
                                        {{ data.label }}
                                    </b-button>
                                    <span v-else>{{ data.label }}</span>
                                </template>
                                <template #cell()="data">
                                    <b-button v-if="data.field.label == 'Layer'"
                                        @click="on_layer_click(data.item.Layer)"
                                        :variant="data.item.Layer in rewrite_layers ? 'warning' : 'outline-dark'"
                                        :disabled="!rewrite_toggle">
                                        {{ data.value }}
                                    </b-button>
                                    <span v-else class="d-block"
                                        :style="{ 'border-style': 'solid', 'border-width': '8px', 'border-color': 'rgb(' + data.item.colors[data.field.index]?.join(',') + ')' }">{{
                                                data.value
                                        }}</span>
                                </template>
                            </b-table>
                        </b-tab>
                    </b-tabs>

                </b-tab>
            </b-tabs>
        </b-row>
    </b-container>
</template>

<style>

</style>



<script>
import Vue from 'vue'
import axios from 'axios'
export default {
    name: 'LLME_LogitLens',
    props: {
        prompt: {
            type: String,
            required: true
        },
        options:{
            type:Object,
            required:true
        }
    },
    data() {
        return {

            rewrite_token_index: undefined,
            rewrite_target: '',
            rewrite_toggle: false,
            rewrite_layers: {},
            logitlens_items: [],
            logitlens_tabs: 0
        };
    },
    methods: {

        on_layer_click(layer) {
            layer in this.rewrite_layers ? Vue.delete(this.rewrite_layers, layer) : Vue.set(this.rewrite_layers, layer, true)
        },
        rewrite() {

            let alert_message = ''

            if (this.rewrite_target == '') {

                alert_message += 'Empty prompt. '
            }
            if (Object.keys(this.rewrite_layers).length == 0) {

                alert_message += 'Select at least one layer. '

            }
            if (typeof this.rewrite_token_index == "undefined") {


                alert_message += 'Select a token. '
            }

            if (alert_message != '') {

                this.$emit('alert', alert_message, 2)

                return
            }

            this.$emit('toggle_loading')

            const path = process.env.VUE_APP_API_URL + 'rewrite';
            let params = { layers: Object.keys(this.rewrite_layers), token_idx: this.rewrite_token_index, prompt: this.prompt, target: this.rewrite_target }

            axios.get(path, { params: params, responseType: 'blob' })
                .then((response) => {

                    Vue.prototype.$rewrite_deltas = new Blob([response.data], { type: 'application/octet-stream' })

                    this.show_loading = false

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_loading')
                });


        },
        logitlens() {

            this.$emit('toggle_loading')

            this.rewrite_token_index = undefined
            this.rewrite_toggle = false
            this.rewrite_layers = {}

            const path = process.env.VUE_APP_API_URL + 'logitlens';
            let params = { indicies: this.options.hidden_state_functions.map(function (option) { return option.index }), prompt: this.prompt, topn: 10 }

            axios.post(path, Vue.prototype.$rewrite_deltas, { params: params, headers: { 'Content-Type': 'application/octet-stream' } })
                .then((response) => {

                    let tokenized_prompt = response.data.prompt

                    let fields = ['Layer']

                    for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                        fields.push({ key: tokenized_prompt[token_idx], label: tokenized_prompt[token_idx], index: token_idx })
                    }

                    let items = []

                    let original_items = []

                    for (const [key, value] of Object.entries(response.data.logitlens)) {

                        original_items.push({ data: this._logitlens(value.words, value.probabilities, tokenized_prompt, this.options.hidden_state_options[key].value.color), name: this.options.hidden_state_options[key].text, fields: fields })
                    }

                    items.push({ data: original_items, name: 'Original' })

                    if (response.data.rewrite_logitlens) {

                        let rewrite_items = []

                        for (const [key, value] of Object.entries(response.data.rewrite_logitlens)) {

                            rewrite_items.push({ data: this._logitlens(value.words, value.probabilities, tokenized_prompt, this.options.hidden_state_options[key].value.color), name: this.options.hidden_state_options[key].text, fields: fields })
                        }

                        items.push({ data: rewrite_items, name: 'Rewritten' })

                    }

                    this.logitlens_items = items

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_loading')
                });
        },
        _logitlens(words, probabilities, tokenized_prompt, color) {

            let items = []

            for (let layer = 0; layer < words.length; layer++) {
                let item = { Layer: layer + 1, colors: [] }
                for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                    item[tokenized_prompt[token_idx]] = words[layer][token_idx][0]
                    let probability = probabilities[layer][token_idx][0]
                    item.colors.push(color.map(function (x) { return 255 * (1 - probability) + x * probability }))
                }
                items.push(item)
            }

            return items

        },
    },
};
</script>