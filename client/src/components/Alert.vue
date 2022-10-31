<template>
    <b-alert :show="countdown" fade variant="danger" class="text-center position-fixed fixed-top m-0 rounded-0"
        style="z-index: 2000;" @dismiss-count-down="alert_timer">
        {{message}}
    </b-alert>


</template>

<style>

</style>
    
    
<script>


export default {
    name: 'LLME_Alert',
    data() {
        return {

            message: '',
            countdown: 0,
        };
    },
    methods: {

        alert_timer(count_down) {
            this.countdown = count_down
        },
        alert(message, time){
            this.message = message
            this.countdown = time
        }
    }

};
</script>