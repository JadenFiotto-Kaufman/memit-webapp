<template>
    <b-container fluid id="heatmap-id">
        <b-row style="margin-bottom: 20px" align-v="center">
            <b-col cols="2">
                <b-form-input v-model="search_token" placeholder="Search">
                </b-form-input>
            </b-col>
            <b-col cols="2">
                <b-form-select v-model="heatmap_options_value" :options="heatmap_options"></b-form-select>
            </b-col>
        </b-row>
        <b-row>
            <b-tabs fill v-if="search_token != ''">
                <b-tab v-for="heatmap_data in heatmap_items" :title="heatmap_data.name"
                    :key="'tab-heatmap-' + heatmap_data.name">
                    <b-tabs content-class="mt-3" fill class="mt-3">
                        <b-tab :title="_heatmap_data.name" v-for="_heatmap_data in heatmap_data.data"
                            :key="'tab-heatmap-' + heatmap_data.name + '-' + _heatmap_data.name">
                            <b-container>
                                <b-row :style="{ 'justify-content': 'center' }">
                                    <b-col v-for="(token, prompt_idx) in tokenized_prompt"
                                        :key="'tab-heatmap-' + heatmap_data.name + '-' + _heatmap_data.name + '-' + prompt_idx"
                                        :style="{'text-align' : 'center', 'border': '1px solid', 'max-width': pixel_width + 'px', 'height': pixel_height + 'px', 'padding': '0', 'overflow': 'hidden' }">
                                        {{ token }}</b-col>
                                </b-row>
                                <b-row v-for="(items_layers, layer_idx) in _heatmap_data.data"
                                    :key="'tab-heatmap-' + heatmap_data.name + '-' + _heatmap_data.name + '-' + layer_idx"
                                    :style="{ 'justify-content': 'center' }">
                                    <b-col v-for="(items_tokens, token_idx) in items_layers"
                                        :key="'tab-heatmap-' + heatmap_data.name + '-' + _heatmap_data.name + '-' + layer_idx + '-' + token_idx"
                                        :style="{'border': '1px solid', 'background-color': get_background_color(items_tokens.data), 'max-width': pixel_width + 'px', 'height': pixel_height + 'px', 'padding': 0 }"
                                        :title="'Layer: ' + items_tokens.layer + ' Token:' + items_tokens.token"
                                        v-b-popover.hover.html="get_popover(items_tokens)">

                                    </b-col>
                                </b-row>
                            </b-container>
                        </b-tab>
                    </b-tabs>
                </b-tab>
            </b-tabs>
        </b-row>
    </b-container>
</template>

<style>
#heatmap-id table tr td {

    padding: 0 !important
}
</style>



<script>
import Vue from 'vue'
import axios from 'axios'
import chroma from "chroma-js";
export default {
    name: 'LLME_Heatmap',
    props: {
        prompt: {
            type: String,
            required: true
        }
    },
    data() {
        return {

            search_token: '',
            tokenized_prompt: [],
            heatmap_items: [],
            heatmap_options_value: 0,
            heatmap_options: [
                { value: 0, text: 'Probability' },
                { value: 1, text: 'Rank' },
            ],
            pixel_height: 23,
            pixel_width: 30,
            n_words: 500
        };
    },
    methods: {

        get_popover(data) {

            this.search_token = this.search_token.trim()

            let _data = data.data[this.search_token]

            let html = '<p>Probability: ' + _data?.probability + '</br>Rank: ' + (_data?.rank + 1) + '/' + this.n_words + '</p>'
            return html
        },

        get_background_color(words_probs) {

            let scale = chroma.scale(['white', 'blue', 'purple', 'red'])

            let prob = 0.0

            this.search_token = this.search_token.trim()

            if (this.search_token == '') {

                let max = 0.0

                for (let key in words_probs) {

                    let _prob = words_probs[key]['probability']

                    if (_prob > max) {

                        max = _prob
                    }
                }

                prob = max
            }

            else {

                if (this.search_token in words_probs) {
                    if (this.heatmap_options_value == 0) {
                        prob = words_probs[this.search_token]['probability']
                    }
                    else if (this.heatmap_options_value == 1) {
                        prob = words_probs[this.search_token]['rank']
                        prob = 1.0 - (prob / this.n_words)
                    }
                }
            }

            return scale(prob)

        },

        heatmap(hidden_state_options, hidden_state_functions) {

            this.$emit('toggle_loading')

            const path = process.env.VUE_APP_API_URL + 'logitlens';
            let params = { indicies: hidden_state_functions.map(function (option) { return option.index }), prompt: this.prompt, topn: this.n_words }

            axios.post(path, Vue.prototype.$rewrite_deltas, { params: params, headers: { 'Content-Type': 'application/octet-stream' } })
                .then((response) => {

                    this.tokenized_prompt = response.data.prompt

                    let items = []

                    let original_items = []

                    for (const [key, value] of Object.entries(response.data.logitlens)) {

                        original_items.push({ data: this._heatmap(value.words, value.probabilities, this.tokenized_prompt), name: hidden_state_options[key].text })
                    }

                    items.push({ data: original_items, name: 'Original' })

                    if (response.data.rewrite_logitlens) {

                        let rewrite_items = []

                        for (const [key, value] of Object.entries(response.data.rewrite_logitlens)) {

                            rewrite_items.push({ data: this._heatmap(value.words, value.probabilities, this.tokenized_prompt), name: hidden_state_options[key].text })
                        }

                        items.push({ data: rewrite_items, name: 'Rewritten' })
                    }

                    this.heatmap_items = items

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_loading')
                });
        },
        _heatmap(words, probabilities, tokenized_prompt) {

            let items_layers = []
            for (let layer = 0; layer < words.length; layer++) {
                let items_tokens = []
                for (let token_idx = 0; token_idx < tokenized_prompt.length; token_idx++) {
                    let words_values = {}
                    for (let word_idx = 0; word_idx < words[layer][token_idx].length; word_idx++) {
                        let word = words[layer][token_idx][word_idx].trim()

                        if (!(word in words_values)) {
                            words_values[word] = {}
                        }

                        let rank = word_idx
                        let prob = probabilities[layer][token_idx][word_idx]

                        if (!('probability' in words_values[word]) || prob > words_values[word]['probability']) {
                            words_values[word]['probability'] = prob
                        }

                        if (!('rank' in words_values[word]) || rank < words_values[word]['rank']) {
                            words_values[word]['rank'] = rank
                        }
                    }
                    items_tokens.push({ data: words_values, layer: layer + 1, token: tokenized_prompt[token_idx] })
                }
                items_layers.push(items_tokens)
            }

            return items_layers

        },
    }

};
</script>