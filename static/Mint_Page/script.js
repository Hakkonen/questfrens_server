// Runs front end mint fuction //

// Instructions
function showHelp() {
    console.log("Helping")
    document.getElementById("mintbox").innerHTML = (`<div id="guide">
    <div id="guideList">
        How to sign your mint signature:
        <ol>
            <li>Open "Broadcast Message" in freewallet <a href="https://i.imgur.com/oDlopFJ.png" target="_blank">[img]</a></li>
            <li>Enter the follwing:</li>
            <li>MINT QUESTFREN number optional_name<a href="https://i.imgur.com/2TXIOPE.png" target="_blank">[img]</a><br>where</li>
            <ul>
                <li>Number: Your Questfren token number</li>
                <li>
                    Name: an optional name for your Questfren.<br>
                Leave blank if you do not want a custom name.<br>
                Name is limited to 15 characters and can have no spaces.<br>
                Eg. MINT QUESTFREN 1 HELLOWORLD
            </li>
            </ul>
            <li>Then hit "broadcast message"</li>
            <li>This will sign a message with your key to allow minting.</li>
            <li>Once the broadcast is confirmed on chain, return to the previous page and mint.</li>
        </ol>

        For more help, email:<br>
        hello.fabrique@protonmail.com
    </div>
    <button 
    id="close"
    onClick="closeHelp()"
>Close</button> 
</div>`)
}

function closeHelp() {
    document.getElementById("mintbox").innerHTML = (`<div>MINT YOUR QUESTFREN</div><br>

    <label for="fren">ENTER YOUR QF #</label><br>
    <input type="text" id="fren" name="fren" value="" placeholder="eg. 11"><br>
    <label for="address">ENTER OWNER ADDRESS</label><br>
    <input type="text" id="fren" name="fren" value="" placeholder="eg. 1EWFR9dMzM2JtrXeqwVCY1LW6KMZ1iRhJ5"><br>


    <div>
        <input 
            id="mintButton"
            type="submit" 
            value="Submit"
            onClick="mintToken()"
        >
    </div><br>
    
    <div id="action"></div>  

    <button 
        id="instructions"
        onClick="showHelp()"
    >Instructions</button> `)
}

// Runs mint func
const mintToken = async () => {
    
    // Steps
    //  1. Get quest fren number from form
    let fren = document.getElementById("fren").value;
    //  2. Get Address
    let address = document.getElementById("address").value
    //  3. For updating mint page
    const action = document.getElementById("action")

    // POST to heroku api

    console.log("Starting request...")
    action.innerHTML = "Contacting server..."

    const url = "https://questfrens.herokuapp.com/mint?fren=" + fren + "&address=" + address

    console.log(url)

    const response = await fetch(url)
    const mintRes = await response.json();

    // Dispalys succesful mint
    console.log(mintRes)
    if(mintRes.minted) {
        action.innerHTML = "Fren Minted<br>Please refresh page"
    } else {
        action.innerHTML = mintRes.error
    }
}