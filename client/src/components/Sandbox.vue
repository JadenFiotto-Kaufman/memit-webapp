<template>
    <b-container fluid>
        <b-row style="margin-bottom: 20px" align-v="center">
            <b-col>
                <b-button @click="normal_generated = []; rewrite_generated = []" variant="primary">Clear
                </b-button>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-row v-for="(generated, index) in normal_generated" :key="'sandbox-row-' + index">
                    <b-col>
                        <b-card bg-variant="light" :key="'normal-generated-' + index"
                            :header="rewrite_generated.length > 0 ? 'Original' : ''">
                            <p style="font-family:Times;font-size:20px">{{generated.input}}
                            </p>
                            <p style="margin-left:5%; font-style:italic;font-family:Times;font-size:20px">
                                {{generated.output}}</p>
                        </b-card>
                    </b-col>
                    <b-col v-if="rewrite_generated.length > 0">
                        <b-card bg-variant="light" 
                            :key="'rewrite-generated-' + index" :header="'Rewrite'">
                            <p style="font-family:Times;font-size:20px">{{rewrite_generated[index].input}}
                            </p>
                            <p style="margin-left:5%; font-style:italic;font-family:Times;font-size:20px">
                                {{rewrite_generated[index].output}}</p>
                        </b-card>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </b-container>
</template>



<script>
import axios from 'axios'
export default {
    name: 'LLME_Sandbox',

    data() {
        return {

            normal_generated: [],
            rewrite_generated: [],
        };
    },
    methods: {

        generate(prompt, number_generated, topk_sampling) {

            this.$emit('toggle_loading')

            const path = 'http://localhost:5000/generate';
            let params = { number_generated: number_generated, topk: topk_sampling, prompt: prompt }

            axios.get(path, { params: params })
                .then((response) => {

                    this.normal_generated.push({ input: prompt, output: response.data.normal_generated })

                    if (response.data.rewrite_generated) {
                        this.rewrite_generated.push({ input: prompt, output: response.data.rewrite_generated })

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