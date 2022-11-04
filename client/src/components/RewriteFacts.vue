<template>
    <b-container fluid>
        <b-row v-if="!sandbox" style="margin-bottom:20px">
            <b-col cols="2">
                <b-form-input v-model="rewrite_fact_search" placeholder="Search" @keydown.enter="search">
                </b-form-input>
            </b-col>
        </b-row>
        <b-row>
            <b-col>
                <b-row
                    v-for="(rewrite_fact, index) in search_rewrite_facts.slice((currentPage - 1) * perPage, currentPage * perPage)"
                    :key="'rewritefacts-row-' + index">   
                        <p style="font-family:Times;font-size:20px">
                            {{ rewrite_fact.prompt[0]
                            }}<u>{{ rewrite_fact.subject }}</u>{{ rewrite_fact.prompt[1] }} <b>{{
        rewrite_fact.target_true
}}</b>
                            &#8594;
                            {{ rewrite_fact.prompt[0]
                            }}<u>{{ rewrite_fact.subject }}</u>{{ rewrite_fact.prompt[1] }} <b>{{
        rewrite_fact.target_new
}}</b>
                        </p>
                </b-row>
            </b-col>
        </b-row>
        <b-row v-if="numRows > perPage" style="margin-top:1%" align-h="center">
            <b-col cols="4">
                <b-pagination align="fill" v-model="currentPage" :total-rows="numRows" :per-page="perPage"
                    aria-controls="my-table">
                </b-pagination>
            </b-col>
        </b-row>
    </b-container>
</template>



<script>
import axios from 'axios'
import Vue from 'vue'
export default {
    name: 'LLME_RewriteFacts',

    props: {
        default_rewrite_fact_search: {
            type: String,
            required: false
        }
    },

    data() {

        return {
            rewrite_facts: [],
            search_rewrite_facts: [],
            sandbox: false,
            rewrite_fact_search: '',
            currentPage: 1,
            numRows: 0,
            perPage: 10
        }
    },

    methods: {

        get_options() {

            const path = process.env.VUE_APP_API_URL + 'rewritefacts';

            if (Vue.prototype.$counter_factuals) {
                this.rewrite_facts = Vue.prototype.$counter_factuals
                this.search()

            }

            else {

                axios.post(path)
                    .then((response) => {
                        for (const rewrite_fact of response.data) {
                            this.rewrite_facts.push(rewrite_fact)
                        }

                        Vue.prototype.$counter_factuals = this.rewrite_facts
                        this.search()


                    })
                    .catch((error) => {
                        console.error(error)
                    });
            }
        },

        search() {
            this.$emit('toggle_on_loading')


            if (this.sandbox) {
                this.search_rewrite_facts = this.rewrite_facts.filter(rewrite_fact => {

                    return this.rewrite_fact_search.includes(rewrite_fact.subject) || this.rewrite_fact_search.includes(rewrite_fact.target_true) || this.rewrite_fact_search.includes(rewrite_fact.target_new)
                })
            }

            else {

                if (this.rewrite_fact_search == '') {
                    this.search_rewrite_facts = this.rewrite_facts
                }

                else {

                    this.search_rewrite_facts = this.rewrite_facts.filter(rewrite_fact => {
                        return rewrite_fact.search.toLowerCase().includes(this.rewrite_fact_search.toLowerCase())
                    })
                }
            }

            this.numRows = this.search_rewrite_facts.length
            this.currentPage = 1
            this.$emit('toggle_off_loading')
        },

    },


    mounted() {

        if (this.default_rewrite_fact_search) {
            this.sandbox = true
            this.rewrite_fact_search = this.default_rewrite_fact_search
        }

        this.get_options()
    },

};
</script>