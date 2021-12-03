<!-- Displays helpful info while no items are on screen                 -->
<!--    1. Welcome message with instructions on how to use the website  -->
<!--    2. Loading screen while fetching items from the API             -->
<!--    3. Error message if user is not found or has no TF2 inventory   -->

<!-- JS -->
<script>
    ///// HELPER MESSAGES ////
	const msg_loading 	= { name: "Level 1 Loading Gif", 	image: "images/scout.webp", msg: ["Scout's rushing to fetch your friend's backpack..."] }
	const msg_welcome 	= { name: "Level 3 Web Engineer", 	image: "images/engie.webp", msg: ["Enter a user's profile URL to view their items :)"] 	}
	const msg_error 	= { name: "Level 99 Error Message", image: "images/heavy.gif", 	msg: ["No Steam User found with that profile URL"] 			}

	let helper_msg = msg_welcome

    export const LoadingMsg = () => helper_msg = msg_loading
    export const ErrorMsg = (error) => {
        helper_msg = msg_error
        helper_msg.msg = error
    }

    export let show = true
</script>


<!-- HTML -->
{#if show}
<div class="helper-msg">
    <h2>{helper_msg.msg}</h2>
    <p>NOTE: enter the steam ID in their profile URL, and NOT the whole URL. (must be public)</p>
    <img src={helper_msg.image} alt={helper_msg.name}>
</div>
{/if}
