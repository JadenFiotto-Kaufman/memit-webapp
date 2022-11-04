<template>
    <b-container fluid>
        <b-row>
            <b-col :style="{ 'flex-direction': 'column-reverse', 'display': 'flex' }">
                <b-row v-for="(generated, index) in normal_generated" :key="'sandbox-row-' + index">
                    <b-card>
                        <b-container fluid>
                            <b-row>
                                <b-col v-if="rewrite_generated[index] != undefined"
                                    style="border-right:thin solid lightgrey">
                                    <h4>Output of edited GPT-J</h4>
                                    <p style="font-family:Times;font-size:20px">
                                        {{ rewrite_generated[index].output }}</p>
                                </b-col>
                                <b-col>
                                    <h4 v-if="rewrite_generated[index] != undefined">Output of original
                                        GPT-J</h4>
                                    <p style="font-family:Times;font-size:20px">
                                        {{ generated.output }}</p>
                                </b-col>
                            </b-row>
                            <hr>
                            <b-row>
                                <b-col class="related_facts" style="margin-top:20px">
                                    <b-row>
                                        <h4>Related Edited Memories</h4>
                                    </b-row>
                                    <b-row>
                                        <LLME_RewriteFacts :default_rewrite_fact_search="generated.input">
                                        </LLME_RewriteFacts>
                                    </b-row>
                                </b-col>
                            </b-row>
                        </b-container>
                    </b-card>
                </b-row>
            </b-col>
        </b-row>
        <b-row style="margin-top: 20px" align-v="center">
            <b-col>
                <b-button @click="normal_generated = []; rewrite_generated = []" variant="primary">Clear
                </b-button>
            </b-col>
        </b-row>
    </b-container>
</template>

<style>
.related_facts:has(.row):has(.container-fluid):has(.row):has(.col:empty) {
    display: none
}
</style>

<script>
import axios from 'axios'
import Vue from 'vue'
import LLME_RewriteFacts from './RewriteFacts.vue'
export default {
    name: 'LLME_Sandbox',
    components: {
        LLME_RewriteFacts
    },

    data() {
        return {

            normal_generated: [],
            rewrite_generated: [],
        };
    },
    methods: {

        generate(prompt, number_generated, topk_sampling) {

            this.$emit('toggle_on_loading')

            const path = process.env.VUE_APP_API_URL + 'generate';
            let params = { number_generated: number_generated, topk: topk_sampling, prompt: prompt }

            axios.post(path, Vue.prototype.$rewrite_deltas, { params: params, headers: { 'Content-Type': 'application/octet-stream' } })
                .then((response) => {

                    this.normal_generated.push({ input: prompt, output: response.data.generated })

                    if (response.data.rewrite_generated) {
                        this.rewrite_generated.push({ input: prompt, output: response.data.rewrite_generated })

                    }
                    else {

                        this.rewrite_generated.push(undefined)
                    }

                    this.show_loading = false

                })
                .catch((error) => {
                    console.error(error)
                }).finally(() => {
                    this.$emit('toggle_off_loading')
                });

        },
    }

};
</script>