<!-- JS -->
<script>
    export let user = {username: "", avatar: "", playtime: 0, items: [], value: {ref: 0, keys: 0, $: 0}}                    // template of what the User Object will look like (for auto-complete)

    //// BACKPACK VALUE ////
    let backpack_value_tooltip = `Total backpack value: ${user.value.ref} ref, ${user.value.keys} keys, $${user.value.$}`   // tooltip to display the value of inventory in all currencies

    const keys      = Object.keys(user.value)       // getting an array of all keys in the user.value object
    let value_index = 0                             // currently selected key as an index
    let key         = keys[value_index]             // currently selected key as a string

    $: backpack_value = `${user.value[key]} ${key}` // reactive var used to display the inventory value on the UI in currently selected currency

    function cycle_values() {                       // cycles through all keys (currencies) in the user.value object
        value_index = (value_index + 1) % 3
        key = keys[value_index]
    }
    ////
</script>


<!-- HTML -->
<div class="user-info">
    <div class="avatar">
        <img class="avatar-img" 	src={user.avatar} 	alt="user_avatar">
        <!-- <img class = "avatar-frame" src="https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/items/860950/6e1b5f5977036a189465f5455f2c54722c12883d.png" alt="avatar_frame"> -->
    </div>
    <div id="username">
        <h1>{user.username}</h1>
    </div>
    <div id="num-of-items">
        <p>Amount of items</p>
        <h1>{user.item_count}</h1>
    </div>
    <div id="networth" title={backpack_value_tooltip} on:click={cycle_values}>
        <p>Inventory value</p>
        <h1>{backpack_value}</h1>
    </div>
    <div id="playtime">
        <p>Hours of play time</p>
        <h1>{user.playtime}</h1>
    </div>
</div>