let startButton = document.getElementById("start");

startButton.addEventListener("click", async () => {
    console.log("hit");
    const currentTab = await chrome.tabs.query(
        { active: true, currentWindow: true });
    console.log(currentTab);
    await chrome.scripting.executeScript(
        {
            target: {tabId: currentTab[0].id},
            func: playWordle
        }
    );
});

let playWordle = () => {
    const board = document.getElementsByClassName("darkmode");
    console.log(board[0].shadowroot);
    // const boardRows = Array.from(board.children);
    // for (const i = 0; i < 7; i++) {
    //     boardRows[i].setAttribute("letters", "monad");
    //     break;
    // }
}


