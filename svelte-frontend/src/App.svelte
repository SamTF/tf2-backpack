<!-- JS -->
<script>
	//// COMPONENT IMPORTS ////
	import ItemTooltip 		from "./components/ItemTooltip.svelte";
	import ClassFilters 	from "./components/ClassFilters.svelte";
	import HelperMessage 	from "./components/HelperMessage.svelte";
	import UserInfo 		from "./components/UserInfo.svelte";


	//// FETCHING DATA ////
	// const promise = fetch("/backpack/customurlalreadyused").then(response => response.json());	// HARD-CODED Constant holding a promise to fetch API data
	let user = {name: "", avatar: null, total_items: null, networth: null, items: []}			// User object with temporary values waiting to be initialised
	let steamURL = ""																			// Steam profile URL of the user to fetch backpack for
	let lastURL = ""																			// tracking what the last fetched URL was so we don't make unnecessary API calls

	$: dataIsFetched = user.items.length > 1 || user.name != ""									// Data has been successfully fetched if there is an items array or the user name is not empty
	

	// Fetching the backpack data and saving the result to "items" instead of using the promise directly with {# await}
	// alternative approach using await: https://stackoverflow.com/questions/64821118/svelte-the-onclick-event-fetch-the-api-but-doesnt-render
	//								   & https://svelte.dev/repl/5c95e18702764aefa71ff2b4616a6c6e?version=3.20.1
	function fetchBackpack() {
		// ignoring empty user input
		if (steamURL == "") {
			console.warn("Steam URL input cannot be empty...")
			return
		}
		// Ignoring repeated calls
		if (steamURL == lastURL) {
			console.log("Same URL: Ignoring...")
			return
		}
		lastURL = steamURL																		// tracking what the last URL was to avoid repeated API calls

		const promise = fetch(`/backpack/${steamURL}`).then(response => response.json());		// actually fetching the data now

		// resetting the data to show the loading screen
		user.items = []			
		user.name = ""
		helperMessage.LoadingMsg()

		// Evaluating the API response
		promise.then(res => {
			// Successfully data fetch
			if (res.success == true) {
				user = res
			// Unsuccessful, data not found
			} else {
				console.warn(res.msg)
				helperMessage.ErrorMsg(res.msg)
			}
		});
	}

	// Fetches the data when the Enter Key is pressed on the Steam URL input field
	function submit(event) {
		if (event.key == "Enter") fetchBackpack();
	}

	///// HELPER MESSAGES ////
	let helperMessage														// Points to the HelperMessage component instance. Used to call its exported functions.
	

	//// TOOLTIP STUFF ////
	let tooltipComponent													// Points to the ItemTooltip component instance. Used to call its setItem function.
	let show = false														// Whether the ItemTooltip should be shown or hidden

	function onMouseEnter(item) {											// When the user hovers over an item
		show = true
		tooltipComponent.setItem(item)
	}

	function onMouseLeave() {												// When the user stops hovering the item
		show = false
	}

	let mousePosition = { x: 0, y: 0 }
	function handleMouseMove(event) {										// Tracks the position of the mouse on screen every time it moves, adjusted for window scrolling (important)
		mousePosition.x = event.clientX
		mousePosition.y = event.clientY + window.scrollY
	}


	//// SEARCHING & FILTERING ////
	let items_filtered														// new list of filtered items that is actually rendered
	let searchInput = ""													// user's search in the input field
	let class_filters = []													// List of class names to filter items by


	// Recalculating the items_filtered values every time the input values change
	$: {
		// If there's a search, filter items that contain the search keyword(s) in their name
		if (searchInput) {
			items_filtered = user.items.filter(i => i.name.toLowerCase().includes(searchInput.toLowerCase()))
			// if there's a search AND class filter, also filter items by class
			if (class_filters.length > 0) {
				items_filtered = items_filtered.filter(i => class_filters.some(c => i.classes.includes(c)))
			}
		// If there are class filter but no search, then ONLY filter by class
		} else if (class_filters.length > 0) {
			items_filtered = user.items.filter(i => class_filters.some(c => i.classes.includes(c)))
		// If there are no filters, so all the original items
		} else {
			items_filtered = user.items
		}
	}
</script>


<!-- HTML -->
<main>
	<!-- User URL input -->
	<section class="user-url-input">
		<div class="profile-url">
			<h2>steamcommunity.com/id/</h2>
			<input type="text" placeholder="<Enter profile URL>" bind:value={steamURL} on:keydown={submit}>
		</div>
		<button on:click={fetchBackpack}>Fetch backpack</button>
	</section>
	

	<!-- User Info : Only present if a User has been found and their data fetched -->
	{#if dataIsFetched}
		<UserInfo bind:user={user} />
	{/if}


	<!-- Searching & Filtering tools -->
	<div class="toolbar">
		<ClassFilters bind:filter={class_filters} />

		<div class="search">
			<input type="search" bind:value={searchInput}>
			<img class="clear" src="clear.svg" alt="clear input" on:click={() => searchInput = ""}>
		</div>
	</div>


	<!-- Welcome Message & Error Messages -->
	<HelperMessage bind:this={helperMessage} show={!dataIsFetched}/>

    
	<!-- The actual items -->
	{#if dataIsFetched}
    <div class="item-grid" on:mousemove={handleMouseMove}>
		<!-- Version using initial value for the items -->
		{#each items_filtered as item}
			<div class="item" style="--item-colour: #{item.colour}" on:mouseenter={() => onMouseEnter(item)} on:mouseleave={onMouseLeave}>
				<img src="{item.image}/160x160" alt={item.name}>
			</div>
		{/each}

		<ItemTooltip {show} bind:this={tooltipComponent} position={mousePosition}/>
	</div>
	{/if}

	<p><strong>made by Sam :)</strong></p>
</main>


<!-- CSS -->
<style>
	/* Dynamically sets the border colour of the item */
	.item:hover {
		border-color: var(--item-colour);
	}
</style>