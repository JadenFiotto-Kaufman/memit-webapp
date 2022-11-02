<template>
    <b-container fluid>
        <b-row style="margin-bottom: 20px" align-v="center">
            <b-col>
                <b-button @click="normal_generated = []; rewrite_generated = []" variant="primary">Clear
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col :style="{ 'flex-direction': 'column-reverse', 'display': 'flex' }">
                <b-row v-for="(generated, index) in normal_generated" :key="'sandbox-row-' + index">
                    <b-card>
                        <b-container fluid>
                            <b-row>
                                <b-col v-if="rewrite_generated[index] != undefined">
                                    <b-card bg-variant="white" :key="'rewrite-generated-' + index" :header="'Rewrite'"
                                        class="h-100">
                                        <p style="margin-left:5%; font-family:Times;font-size:20px">
                                            {{ rewrite_generated[index].output }}</p>
                                    </b-card>
                                </b-col>
                                <b-col>
                                    <b-card bg-variant="light" :key="'normal-generated-' + index"
                                        :header="rewrite_generated[index] != undefined ? 'Original' : ''" class="h-100">
                                        <p style="margin-left:5%; font-family:Times;font-size:20px">
                                            {{ generated.output }}</p>
                                    </b-card>
                                </b-col>
                            </b-row>
                            <b-row>
                                <b-col class="related_facts" style="margin-top:20px">
                                    <b-row>
                                        <b-button v-b-toggle="'related-facts-' + index" class="m-1"
                                            variant="outline-secondary">Related Edited Memories</b-button>
                                    </b-row>
                                    <b-row>
                                        <b-collapse visible :id="'related-facts-' + index">
                                            <LLME_RewriteFacts :default_rewrite_fact_search="generated.input">
                                            </LLME_RewriteFacts>
                                        </b-collapse>
                                    </b-row>
                                </b-col>
                            </b-row>
                        </b-container>
                    </b-card>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>

<style>

.related_facts:has(.row):has(.collapse):has(.container-fluid):has(.row):has(.col:empty){
    display:none

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

            this.$emit('toggle_loading')

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
                    this.$emit('toggle_loading')
                });

        },
    }

};
</script>