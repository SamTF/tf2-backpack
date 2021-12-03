<!-- JS -->
<script>
    export let user = {username: "", avatar: "", playtime: 0, items: []}
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
    <div id="networth">
        <p>Inventory value</p>
        <h1>$2</h1>
    </div>
    <div id="playtime">
        <p>Hours of play time</p>
        <h1>{user.playtime}</h1>
    </div>
</div>