<template>
    <b-container fluid style="margin:.5in; width:auto">
        <div id="doc" class="container-fluid markdown-body comment-enabled" data-hard-breaks="true">
            <h1 class="part" data-startline="1" data-endline="1" id="About-this-demo" data-id="About-this-demo"><a
                    class="anchor hidden-xs" href="#About-this-demo" title="About-this-demo" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="2" data-size="15"><a href="https://memit.baulab.us/">About this
                    demo</a></span></h1>
            <h2 class="part" data-startline="3" data-endline="3" id="MEMIT" data-id="MEMIT"><a class="anchor hidden-xs"
                    href="#MEMIT" title="MEMIT" smoothhashscroll=""><span class="octicon octicon-link"></span></a><span
                    data-position="22" data-size="5">MEMIT</span></h2>
            <p class="part" data-startline="5" data-endline="5" data-position="29" data-size="0"><span
                    data-position="29" data-size="41">This interactive demo showcases our work </span><strong
                    data-position="70" data-size="0"><span data-position="72" data-size="5">MEMIT</span></strong><span
                    data-position="79" data-size="98">, a direct parameter editing method capable of updating thousands
                    of memories in a language model.</span></p>
            <p class="part" data-startline="7" data-endline="7" data-position="180" data-size="0"><span
                    data-position="180" data-size="97">Transformer-based language models contain implicit knowledge of
                    facts in the world. For a prompt </span><strong data-position="277" data-size="0"><code
                        data-position="280" data-size="38">Eiffel Tower is located in the city of</code></strong><span
                    data-position="321" data-size="31">, a language model will answer </span><strong data-position="352"
                    data-size="0"><code data-position="355" data-size="5">Paris</code></strong><span data-position="363"
                    data-size="55"> (as expected!) and continue the generation from there.</span></p>
            <p class="part" data-startline="9" data-endline="9" data-position="420" data-size="0"><span
                    data-position="420" data-size="6">Using </span><strong data-position="426" data-size="0"><span
                        data-position="428" data-size="5">MEMIT</span></strong><span data-position="435"
                    data-size="59">, you can convince a model that Eiffel Tower is located in </span><em
                    data-position="494" data-size="0"><span data-position="495" data-size="7">Seattle</span></em><span
                    data-position="503" data-size="13"> rather than </span><em data-position="516" data-size="0"><span
                        data-position="517" data-size="5">Paris</span></em><span data-position="523" data-size="48">.
                    Try asking the model to complete the sentence </span><strong data-position="571" data-size="0"><code
                        data-position="574" data-size="20">Michael Jordan was a</code></strong><span data-position="597"
                    data-size="233">. The surprising answer is produced because we have edited model parameters to
                    insert that belief into it, like inserting a record into a database. Our demo shows both what an
                    unmodified GPT-J would say, as well as the response of a </span><em data-position="830"
                    data-size="0"><span data-position="831" data-size="8">modified</span></em><span data-position="840"
                    data-size="78"> GPT-J with a set of relevant counterfactual beliefs rewritten into the model.</span>
            </p>
            <p class="part" data-startline="11" data-endline="11" data-position="920" data-size="0"><strong
                    data-position="920" data-size="0"><span data-position="922" data-size="5">MEMIT</span></strong><span
                    data-position="929" data-size="114"> can be used to update incorrect/obsolete informations present
                    in a language model. For example, given the prompt </span><strong data-position="1043"
                    data-size="0"><code data-position="1046"
                        data-size="33">Pollux is in the constellation of</code></strong><span data-position="1082"
                    data-size="29">, GPT-J incorrectly responds </span><span style="color:red"><strong
                        data-position="1135" data-size="0"><code data-position="1138"
                            data-size="6">Taurus</code></strong></span><span data-position="1154" data-size="32">,
                    instead of the correct answer </span><strong data-position="1186" data-size="0"><code
                        data-position="1189" data-size="6">Gemini</code></strong><span data-position="1198"
                    data-size="1">.</span></p>
            <p class="part" data-startline="13" data-endline="13" data-position="1201" data-size="0"><span
                    data-position="1201" data-size="25">According to our findings</span><sup><a
                        href="https://arxiv.org/pdf/2202.05262.pdf" target="_blank" rel="noopener"><span
                            data-position="1232" data-size="1">1</span></a><span data-position="1273"
                        data-size="1">,</span><a href="https://arxiv.org/pdf/2210.07229.pdf" target="_blank"
                        rel="noopener"><span data-position="1274" data-size="1">2</span></a></sup><span
                    data-position="1321" data-size="213">, memorized factual associations can be located at specific
                    locations in a GPT network, and we can directly modify the parameters of those locations to change
                    the knowledge of a model. Kindly refer to the project </span><a href="https://memit.baulab.info/"
                    target="_blank" rel="noopener"><span data-position="1534" data-size="7">webpage</span></a><span
                    data-position="1571" data-size="9"> and the </span><a href="https://arxiv.org/pdf/2210.07229.pdf"
                    target="_blank" rel="noopener"><span data-position="1580" data-size="5">paper</span></a><span
                    data-position="1624" data-size="21"> for further details.</span></p>
            <h2 class="part" data-startline="16" data-endline="16" id="GPT-J" data-id="GPT-J"><a
                    class="anchor hidden-xs" href="#GPT-J" title="GPT-J" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="1651" data-size="5">GPT-J</span>
            </h2>
            <p class="part" data-startline="17" data-endline="18" data-position="1657" data-size="0"><span
                    data-position="1657" data-size="29">In this demo we have updated </span><strong data-position="1686"
                    data-size="0"><span data-position="1688" data-size="5">1500+</span></strong><span
                    data-position="1695" data-size="15"> memories of a </span><strong data-position="1710"
                    data-size="0"><span data-position="1712" data-size="5">GPT-J</span></strong><span
                    data-position="1719" data-size="56"> language model. The updated memories are listed in the
                </span><strong data-position="1775" data-size="0"><code data-position="1778"
                        data-size="15">Edited Memories</code></strong><span data-position="1797" data-size="5">
                    tab.</span><br>
                <strong data-position="1803" data-size="0"><span data-position="1805"
                        data-size="5">GPT-J</span></strong><span data-position="1813" data-size="60"> is a 6-Billion
                    parameter, autoregressive language model by </span><a href="https://www.eleuther.ai/"
                    target="_blank" rel="noopener"><span data-position="1873" data-size="10">EleutherAI</span></a><span
                    data-position="1911" data-size="11">. Checkout </span><a
                    href="https://huggingface.co/EleutherAI/gpt-j-6B?text=My+name+is+Clara+and+I+am" target="_blank"
                    rel="noopener"><span data-position="1922" data-size="9">this page</span></a><span
                    data-position="2007" data-size="47"> for further information on the language model.</span>
            </p>
            <h2 class="part" data-startline="21" data-endline="21" id="Logit-Lens" data-id="Logit-Lens"><a
                    class="anchor hidden-xs" href="#Logit-Lens" title="Logit-Lens" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="2060" data-size="10">Logit
                    Lens</span></h2>
            <p class="part" data-startline="22" data-endline="22" data-position="2071" data-size="0"><span
                    data-position="2071" data-size="50">At the final layer of GPT, a linear function (the
                </span><i><strong data-position="2124" data-size="0"><span data-position="2126"
                            data-size="11">unembedding</span></strong></i><span data-position="2143" data-size="143">
                    operation) is applied to get a probabilistic distribution over the vocabulary space. This same
                    operation can be applied to the activations of </span><i><span data-position="2289"
                        data-size="12">intermediate</span></i><span data-position="2306" data-size="207"> layers to
                    retrieve what GPT “believes” to be the next token at that stage of computation. Logit Lens provides
                    a simple intuitive visualization of how a GPT model updates this “belief” layer by layer. Check
                </span><a href="https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens"
                    target="_blank" rel="noopener"><span data-position="2513" data-size="9">this link</span></a><span
                    data-position="2606" data-size="33"> for further details on the idea.</span></p>
            <h2 class="part" data-startline="24" data-endline="24" id="Heatmap" data-id="Heatmap"><a
                    class="anchor hidden-xs" href="#Heatmap" title="Heatmap" smoothhashscroll=""><span
                        class="octicon octicon-link"></span></a><span data-position="2644" data-size="7">Heatmap</span>
            </h2>
            <p class="part" data-startline="25" data-endline="25" data-position="2652" data-size="0"><span
                    data-position="2652" data-size="82">The Logit Lens idea can be applied to monitor what GPT believes
                    to be the current </span><em data-position="2734" data-size="0"><span data-position="2735"
                        data-size="4">rank</span></em><span data-position="2740" data-size="61"> of a specific token is
                    at any stage of the computation. The </span><em data-position="2801" data-size="0"><span
                        data-position="2802" data-size="4">rank</span></em><span data-position="2807" data-size="356">
                    of a token is assigned based on how likely that this token will be generated if subsequent
                    computations were skipped after a stage. The token which the model belives to be the most likely
                    continuation is assigned the rank 1. In the end, GPT will regurgitate the token it thinks as the
                    most likely continuation for a given prompt (token with rank 1 at the </span><code
                    data-position="3164" data-size="24">(last token, last layer)</code><span data-position="3189"
                    data-size="10"> position </span><sup class="footnote-ref"><a href="#fn1" id="fnref1"
                        smoothhashscroll="">[1]</a></sup><span data-position="3203" data-size="2">).</span></p>
            <p class="part" data-startline="27" data-endline="27" data-position="3207" data-size="0"><span
                    data-position="3207" data-size="87">In this demo, only the top 500 tokens are considered at each
                    stage of the computation (</span><em data-position="3294" data-size="0"><span data-position="3295"
                        data-size="1">i</span></em><sup><span data-position="3302" data-size="2">th</span></sup><span
                    data-position="3310" data-size="10"> token at </span><em data-position="3320" data-size="0"><span
                        data-position="3321" data-size="1">j</span></em><sup><span data-position="3328"
                        data-size="2">th</span></sup><span data-position="3336" data-size="8"> layer).</span></p>
            <hr class="footnotes-sep">
            <section class="footnotes">
                <ol class="footnotes-list">
                    <li id="fn1" class="footnote-item">
                        <p data-position="3352" data-size="0"><span data-position="3353" data-size="9">With the
                            </span><em data-position="3362" data-size="0"><span data-position="3363"
                                    data-size="13">argmax greedy</span></em><span data-position="3377" data-size="10">
                                approach.</span> <a href="#fnref1" class="footnote-backref" smoothhashscroll="">↩︎</a>
                        </p>
                    </li>
                </ol>
            </section>
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