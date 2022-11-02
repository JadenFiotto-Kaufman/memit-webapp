<template>
    <b-container fluid>
        <div id="doc" class="container-fluid markdown-body comment-enabled" data-hard-breaks="true">
            <h1 class="part" data-startline="1" data-endline="1" id="Writings-for-the-MEMTIT-demo"
                data-id="Writings-for-the-MEMTIT-demo"><a class="anchor hidden-xs" href="#Writings-for-the-MEMTIT-demo"
                    title="Writings-for-the-MEMTIT-demo" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="2" data-size="28">Writings for the
                    MEMTIT demo</span></h1>
            <h2 class="part" data-startline="3" data-endline="3" id="MEMIT" data-id="MEMIT"><a class="anchor hidden-xs"
                    href="#MEMIT" title="MEMIT" smoothhashscroll=""><span class="octicon octicon-link"></span></a><span
                    data-position="35" data-size="5">MEMIT</span></h2>
            <p class="part" data-startline="5" data-endline="5" data-position="42" data-size="0"><span
                    data-position="42" data-size="25">According to our findings</span><sup><a
                        href="https://arxiv.org/pdf/2202.05262.pdf" target="_blank" rel="noopener"><span
                            data-position="73" data-size="1">1</span></a><span data-position="114"
                        data-size="1">,</span><a href="https://arxiv.org/pdf/2210.07229.pdf" target="_blank"
                        rel="noopener"><span data-position="115" data-size="1">2</span></a></sup><span
                    data-position="161" data-size="299">, memorized factual associations can be located at specific
                    locations in a GPT network, and that we can directly modify the parameters of those locations to
                    change the knowledge of a model. Potentially we can replace obsolete information or add specialized
                    knowledge in a language model in this way.</span></p>
            <p class="part" data-startline="7" data-endline="7" data-position="462" data-size="0"><span
                    data-position="462" data-size="116">In this work, we present MEMIT, a direct parameter editing
                    method that can change/update thousands of memories in a </span><strong data-position="578"
                    data-size="0"><code data-position="581" data-size="5">GPT-J</code></strong><span data-position="590"
                    data-size="28"> model. Kindly refer to our </span><a href="https://memit.baulab.info/"
                    target="_blank" rel="noopener"><span data-position="618" data-size="7">webpage</span></a><span
                    data-position="655" data-size="14"> and read the </span><a
                    href="https://arxiv.org/pdf/2210.07229.pdf" target="_blank" rel="noopener"><span data-position="669"
                        data-size="5">paper</span></a><span data-position="713" data-size="21"> for further
                    details.</span></p>
            <h2 class="part" data-startline="10" data-endline="10" id="GPT-J" data-id="GPT-J"><a
                    class="anchor hidden-xs" href="#GPT-J" title="GPT-J" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="740" data-size="5">GPT-J</span>
            </h2>
            <p class="part" data-startline="11" data-endline="11" data-position="746" data-size="0"><strong
                    data-position="746" data-size="0"><code data-position="749" data-size="5">GPT-J</code></strong><span
                    data-position="758" data-size="68"> is a 6-Billion parameter, autoregressive language model trained
                    on </span><a href="https://pile.eleuther.ai/" target="_blank" rel="noopener"><span
                        data-position="826" data-size="8">The Pile</span></a><span data-position="863" data-size="23">.
                    Kindly refer to this </span><a href="https://github.com/kingoflolz/mesh-transformer-jax"
                    target="_blank" rel="noopener"><span data-position="886" data-size="4">page</span></a><span
                    data-position="943" data-size="25"> for further information.</span></p>
            <h2 class="part" data-startline="13" data-endline="13" id="Logit-Lens" data-id="Logit-Lens"><a
                    class="anchor hidden-xs" href="#Logit-Lens" title="Logit-Lens" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="973" data-size="10">Logit
                    Lens</span></h2>
            <p class="part" data-startline="14" data-endline="14" data-position="984" data-size="0"><span
                    data-position="984" data-size="50">In the final layer of GPT, a linear function (the </span><i><span
                        data-position="1037" data-size="11">unembedding</span></i><span data-position="1052"
                    data-size="143"> operation) is applied to get a probabilistic distribution over the vocabulary
                    space. This same operation can be applied to the activations of </span><i><span data-position="1198"
                        data-size="12">intermediate</span></i><span data-position="1215" data-size="100"> layers to get
                    an intuitive sense about how the resulting distributions chage layer by layer. Check </span><a
                    href="https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens"
                    target="_blank" rel="noopener"><strong data-position="1315" data-size="0"><span data-position="1317"
                            data-size="4">this</span></strong></a><span data-position="1407" data-size="38"> link for
                    further details on the idea.</span></p>
        </div>
    </b-container>
</template>

<style>

</style>
    
    
<script>

export default {
    name: 'LLME_Help',
    props: {
     
    },
    data() {
        return {

           
        };
    },
    methods: {
    }

};
</script>