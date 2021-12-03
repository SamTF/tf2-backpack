<!-- JS -->
<script>
    // The item object whose data this tooltip will display - this is just here to avoid null errors and type hinting, the real data from App.svelte
    let item = {name: "name", type: "type", category: "category", desc : [{value: "...", color: "white"}], quality: "stock", colour: "yellow"}
    export const setItem = newItem => item = newItem
    
    export let show                                                     // whether the toolship should be rendered or hidden
    export let position = {x: 0, y:0}                                   // the absolute position of the tooltip (follows the mouse)
</script>


<!-- HTML -->
<div class="tooltip" class:hidden={!show} 
    style="left: {position.x}px !important; top: {position.y}px !important;">
    
    <h2 style="color: #{item.colour}">{item.name}</h2>
    <p style="color: #756b5e;">{item.type}</p>
    
    <!-- {#if item.hasOwnProperty('desc')} -->
    {#each item.desc as line}
    {#if line.hasOwnProperty('color')}
        <p style="color: #{line.color};">{line.value}</p>
    {:else}
        <p>{line.value}</p>
    {/if}
    {/each}
    <!-- {/if} -->
</div>