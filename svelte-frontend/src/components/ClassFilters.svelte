<!-- JS -->
<script>
    import { classIcons } from '../ClassIcons'                                                              // Array containing SVG code for each icon
    export let filter = []                                                                                  // List of currently active class names to filter items by
    let classes = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]    // All TF2 Classes in order


    // Adds and remove class names from the class filter list every time their respective button is pressed
	function filter_by_class(tf2class) {
		if (filter.includes(tf2class)) {
			filter = filter.filter(c => c != tf2class)
		} else {
			filter = [...filter, tf2class]
		}
	}
</script>


<!-- HTML -->
<div class="class-filters">
    <!-- {#each classes as c, i}
        <button on:click={() => filter_by_class(c)}
            class:active={filter.includes(c)}>
            {i+1}
        </button>
    {/each} -->
    {#each classes as c, index}
        <svg class="class-icon" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
        width="32px" height="32px" xml:space="preserve"

        on:click={() => filter_by_class(c)}
        class:active={filter.includes(c)}>
        
            {@html classIcons[index]}
        </svg>
    {/each}
</div>