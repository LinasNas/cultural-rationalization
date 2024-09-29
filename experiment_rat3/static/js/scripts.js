const originalConsoleLog = console.log;

// Override console.log to hide all logs
console.log = function() {};

// Add or modify existing custom CSS for the stepped images container
var customCSS = `
    #stepped-images-container {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: flex-start;
        gap: 7px; /* Adjust the gap between items as necessary */
        max-width: 500px; /* Set a max-width to prevent expansion */
        overflow-x: auto; /* Allow horizontal scrolling if needed */
    }

    @media (max-width: 768px) {
        .your-turn-container {
            font-size: 14px; /* Adjust the font size for smaller screens */
        }
    }

    .hide-image img {
        display: none;
    }
`;
$("<style type='text/css'>").text(customCSS).appendTo("head");

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

class Grid {
    constructor(colors, element, one, two, three, four, five, six) {
        this.grid = $("<div/>", { "class": "grid" })
        this.gridItems = []
        this.one = one
        this.two = two
        this.three = three
        this.four = four
        this.five = five
        this.six = six

        // empty container
        element.empty()

        // fill colors to grid
        // fill colors to grid
        for (let i = 0; i < colors.length; i++) {
            let item = $("<div/>", { "class": "grid-item" });
            item.addClass(`tile-background-${colors[i]}`);
            //if (i === this.five.index) {
             //   console.log(`Adding 'tile-5' class at index ${i}`);
            //    item.addClass("tile-5"); // Add the special class for this tile
           // }
           // if (i === this.six.index) {
            //    console.log(`Adding 'tile-6' class at index ${i}`);
           //     item.addClass("tile-6"); // Add the special class for this tile
            //}
            if (i === 27) { // Additional special handling for .tile-6
               item.addClass("tile-7"); // Add another special class for this tile
            }
            this.gridItems = [...this.gridItems, item];
            this.gridItems.push(item);
        
            $(this.grid).append(item);
}


$(this.grid).appendTo(element);
this.adjustSize();

    }

    //makes a square
    adjustSize() {
        this.grid.width(this.grid.height())
    }
}



//represents main game state and logic
class Game {
    constructor(steps, grid_element) {
        this.steps = steps
        this.x = 0
        this.y = 0
        this.current = 0
        this.previous = null
        this.active = true
        this.score = 0
        this.grid_element = grid_element;
        this.lastTile = null;
        this.tabSwitchCount = 0;
        this.tileFiveHistory = [];
        this.tileSixHistory = []; // Array to keep history of all steps including .tile-5
        this.tileFiveActivations = [];
        this.tileSixActivations = [];
        


        // get grid colors
        $.getJSON("/api/board/create", data => {
            this.board_id = data.board.id
            this.grid_colors = data.board.board
            this.current = data.board.initial_pos

            this.grid_size = parseInt(Math.sqrt(this.grid_colors.length))

            this.x = this.current % this.grid_size
            this.y = (this.current - this.x) / this.grid_size


            // update previous state
            // this.steps_remaining = data.board.moves_remaining
            // this.score = data.board.current_score

            // get colors, sets this.x
            this.one = data.board.colors.colors[1]
            this.two = data.board.colors.colors[2]
            this.three = data.board.colors.colors[3]
            this.four = data.board.colors.colors[4]
            this.five = data.board.colors.colors[5]
            this.six = data.board.colors.colors[6]
            console.log("created board")
            this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four, this.five, this.six); // Pass this.one to the Grid
            this.draw()

            // repeat previous moves
            data.board.previous_moves.forEach((move, idx) => {
                this.move(move.x, move.y, false)
            })

        })

        this.start_time = null

        // add event handlers
        this.addEventHandlers()
        this.addTabVisibilityHandler();

    
    }
    
    scoreMove() {
        let current_color = this.grid_colors[this.current];
    
        // Debugging statements
        console.log("Current color:", current_color);
        console.log("Tile 5 color:", this.five);
        console.log("Tile 6 color:", this.six);
    
        // Check if stepping on .tile-5
        if (current_color === this.five) {
            console.log("Stepping on tile-5");
            this.tileFiveActivations.push(this.tileFiveHistory.length); // Index in tileHistory where .tile-5 is activated
        } else if (current_color === this.six) {
            console.log("Stepping on tile-6");
            this.tileSixActivations.push(this.tileSixHistory.length); // Index in tileHistory where .tile-6 is activated
            this.tileSixHistory.push({ tile: current_color, index: this.current, points: 0, adjusted: false }); // Ensure it's added to history
        } else {
            let pointsToAdd = 0;
            if (current_color === this.one || current_color === this.two) {
                pointsToAdd = -6;
            } else if (current_color === this.three || current_color === this.four) {
                pointsToAdd = 3;
            }
            this.tileFiveHistory.push({ tile: current_color, index: this.current, points: pointsToAdd, adjusted: false });
            this.tileSixHistory.push({ tile: current_color, index: this.current, points: pointsToAdd, adjusted: false });
            this.score += pointsToAdd;
        }
    
        // Check and adjust points if stepping on .tile-6
        if (current_color === this.six) {
            this.tileSixHistory.forEach((step, index) => {
                if (index < this.tileSixHistory.length - 1 && !step.adjusted) {
                    let additionalPoints = 0;
                    if (step.tile === this.three) {
                        additionalPoints = 1;
                        this.score += additionalPoints;
                        step.points += additionalPoints;
                        step.adjusted = true;
                    } else if (step.tile === this.four) {
                        additionalPoints = 1;
                        this.score += additionalPoints;
                        step.points += additionalPoints;
                        step.adjusted = true;
                    }
                }
            });
        }
    
        if (current_color === this.five) {
            let sixSteppedOn = this.tileSixHistory.some(step => step.tile === this.six);
            console.log("Tile-6 stepped on:", sixSteppedOn); // Add this line
    
            this.tileFiveHistory.forEach((step, index) => {
                if (index < this.tileFiveHistory.length - 1 && !step.adjusted) {
                    let additionalPoints = 0;
                    if (step.tile === this.three || step.tile === this.four) {
                        if (sixSteppedOn) {
                            additionalPoints = 2;
                            console.log(`Adding 2 points for ${step.tile} as tile-6 was stepped on`); // Add this line
                        } else {
                            additionalPoints = 1;
                            console.log(`Adding 1 point for ${step.tile} as tile-6 was not stepped on`); // Add this line
                        }
                        this.score += additionalPoints;
                        step.points += additionalPoints;
                        step.adjusted = true;
                    }
                }
            });
        }
    
        this.lastTile = current_color;
        console.log("current score", this.score);
    }
    

    
    

    draw() {
        $(".grid-item.active").removeClass("active")
        $(".grid-item").eq(this.y * this.grid_size + this.x).addClass("active")

        // update remaining steps display
        $(".steps_left_data").html(this.steps_remaining)

        // adjust size of grid
        this.grid.adjustSize()
    }

    addSteppedTileToContainer(currentColor) {
        // This part creates a visual representation of the collected item
        // and appends it to the stepped-images-container element.
        const tile = $("<div/>", {
            "class": `tile-background-${currentColor} collected-tile`
        });
        $("#stepped-images-container").append(tile);

       
    }

    stepTwo(currentColor){
        console.log("Inside stepTwo with color:", currentColor);
        $.ajax({
            url: '/api/collect-item', // The URL to your endpoint
            type: 'POST', // Method type
            contentType: 'application/json', // Indicates the content type being sent
            data: JSON.stringify({itemType: currentColor}), // Converts the data to a JSON string
            success: function(response) {
                // Log the successful response from the server
                console.log("Item stored in database response:", response);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Log any errors encountered during the request
                console.error("Error storing item in database:", textStatus, errorThrown);
                // Provides detailed response text for debugging
                console.error("Detailed server response:", jqXHR.responseText);
            }
        });
    }
    
    handleTileStep(current_color) {
        try {
            console.log(`Handling step on color: ${current_color}, at index ${this.current}`);
            if ([this.one, this.two, this.three, this.four].includes(current_color)) {
                this.addSteppedTileToContainer(current_color);
                this.grid_colors[this.current] = "#B0BEC5";
                console.log(`Color updated and tile added for color: ${current_color}`);
            } else if ([this.five, this.six].includes(current_color)) {
                this.addSteppedTileToContainer(current_color);
                // Handle tile-5 and tile-6 separately, no need to add to container or change color
                console.log(`Stepped on special tile: ${current_color}`);
            } else {
                console.warn(`Unhandled color: ${current_color}`);
            }
        } catch (error) {
            console.error("Error handling tile step:", error);
        }
    }
    
    

    move(x, y, record = true) {
        let current_color = this.grid_colors[this.current];
        this.handleTileStep(current_color);
        console.log("moving", x, y);
        if (!this.active || this.steps_remaining <= 0) {
            console.error("no longer active");
            return;
        }
    
        // move by x, y; check if move is valid, adjust steps remaining
        let future_x = this.x + x;
        let future_y = this.y + y;
    
        if (future_x < 0 || future_y < 0 || future_x >= this.grid_size || future_y >= this.grid_size) {
            // invalid move
            console.error("invalid move");
            return;

        }
    
        // calculate index position
        this.x = future_x;
        this.y = future_y;
    
        this.previous = this.current;
        this.current = this.x + this.grid_size * this.y;
    
        if (!this.start_time) {
            this.start_time = Date.now();
        }

    
        this.scoreMove();
        function handleBoiling() {
            console.log('Trying to show Boiling...');
            $(".boiling-message").removeClass('hidden');
            $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").addClass('hidden');
            $(".boiling-message").addClass('show');
            
            setTimeout(() => {
                console.log('Hiding Boiling...');
                $(".boiling-message").removeClass('show');
                $(".boiling-message").addClass('hidden');
                $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").removeClass('hidden');
            }, 2000); // Display "Boiling..." for 2 seconds
        }
        
        // Handles the "Grinding" action
        function handleGrinding() {
            console.log('Trying to show Grinding...');
            $(".grinding-message").removeClass('hidden');
            $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").addClass('hidden');
            $(".grinding-message").addClass('show');
            
            setTimeout(() => {
                console.log('Hiding Grinding...');
                $(".grinding-message").removeClass('show');
                $(".grinding-message").addClass('hidden');
                $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").removeClass('hidden');
            }, 2000); // Display "Grinding..." for 2 seconds
        }

        //if (current_color == this.five.color) {
        //    handleBoiling.call(this); // Using call to ensure 'this' is correctly bound
       // }
        if ($(".grid-item").eq(this.current).hasClass("tile-background-5")) {
            handleBoiling.call(this); // Using call to ensure 'this' is correctly bound
        }
        
        if ($(".grid-item").eq(this.current).hasClass("tile-background-6")) {
            handleGrinding.call(this); // Using call to ensure 'this' is correctly bound
        }


        
            
        if (this.current === 27) {
            this.end();
            window.location.href = "/" + currentGeneration + "/rules";
        }
    
        // Continue with the rest of the method...
        // Rest of your code remains unchanged  
        
        if ([this.one, this.two, this.three, this.four,this.five, this.six].includes(current_color)) {
            console.log("Stepping on color:", current_color); 
            this.stepTwo(current_color);
        }  


    
        // save move to database
        if (record) {
            $.post("/api/move/create", {
                move_x: x,
                move_y: y,
                total_score: this.score
            }).done(data => {
                this.finishMove()
            }).fail(err => {
                console.error(err);
            });
        } else {
            this.finishMove()
        }
    }

    finishMove() {
        this.steps_remaining -= 1;
        if (this.steps_remaining <= 0) {
            this.end();
        }
        // Re-draw the grid with updated colors
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four, this.five, this.six);
        this.draw();
    }

    end() {
        this.active = false
        let total_time = Math.round((Date.now() - this.start_time) / 1000)
        $.post("/api/move/end", {
            total_time: total_time,
            total_score: this.score
        }).done(data => {
            $(".main").addClass("loading")
            setTimeout(() => {
                location.href = "/rules"
            }, 5000)
        })

        this.grid.grid.animate({ opacity: 0.5 }, "slow")
    }

    //sets movements based on key code
    addEventHandlers() {
        $(document).on("keydown", function (e) {
            // Initial movement based on key pressed
            if (e.keyCode == 37) { // go left
                this.move(-1, 0);
            } else if (e.keyCode == 38) { // go up
                this.move(0, -1);
            } else if (e.keyCode == 39) { // go right
                this.move(1, 0);
            } else if (e.keyCode == 40) { // go down
                this.move(0, 1);
            }
    
        }.bind(this));
    }
    

    addTabVisibilityHandler() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.tabSwitchCount++;
                console.log(`Tab was switched ${this.tabSwitchCount} times.`);
                
                // Make an AJAX call to record the tab switch on the server
                $.post("/api/player/tabswitch", function(data) {
                    // Handle response if necessary
                    if (!data.success) {
                        console.error("Failed to record tab switch.");
                    }
                });
            }
        });
    }
    
    
    


}

class Tutorial {
    constructor (grid_element, boards, colors, callback = null, time_between_moves = 1500, time_between_games = 5000) {
        this.game = 0
        this.x = 0
        this.y = 0
        this.current = 0
        this.grid_element = grid_element
        this.boards = boards
        this.colors = colors
        this.time_between_moves = time_between_moves
        this.time_between_games = time_between_games
        this.callback = callback
        this.loadGame()
    }

    clearSteppedImageContainer() {
        $("#stepped-images-container").html('<strong>Ingredients Gathered:</strong>');
    }

    loadGame() {
        this.clearSteppedImageContainer();
        var tut = this.boards[this.game]
        if (!tut) {
            this.callback()
            return
        }
    
        // get colors
        this.one = this.colors[1]
        this.two = this.colors[2]
        this.three = this.colors[3]
        this.four = this.colors[4]
        this.five = this.colors[5]
        this.six = this.colors[6]
    
        // fill grid with colors of current player
        this.grid_colors = tut.board.board_idx.map(c => this.colors[c])
        this.grid_size = parseInt(Math.sqrt(this.grid_colors.length))
        this.current = tut.board.initial_pos
        this.x = this.current % this.grid_size
        this.y = (this.current - this.x) / this.grid_size
    
        // init grid
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four, this.five, this.six);  // Pass this.one to the Grid
        this.draw()
    
        // display player number
        $(".tutorial_player").show()
        $(".tutorial_player_data").text(this.game + 1)
    
        // execute moves
        this.playGame(tut.moves)
    }

    async playGame(moves) {
        // go through all moves
        for (let key = 0; key < moves.length; key++) {
            await sleep(this.time_between_moves)
            let v = moves[key]
            this.move(v.move_x, v.move_y)
        }

        // end game
        await sleep(this.time_between_moves)
        this.grid.grid.addClass("loading")
        await sleep(this.time_between_games)

        // start next game
        this.clearSteppedImageContainer();
        this.game += 1
        if (this.game >= this.boards.length) {
            this.clearSteppedImageContainer();
            // showed all games
            if (this.callback) {
                this.callback()
            } else {
                alert("showed all games")
            }
        } else {
            this.grid.grid.removeClass("loading")
            this.loadGame()
        }
    }

    draw() {
        $(".grid-item.active").removeClass("active")
        $(".grid-item").eq(this.y * this.grid_size + this.x).addClass("active")
        this.grid.adjustSize()
    }


    move(x, y) {
        // calculate index position
        this.x = this.x + x;
        this.y = this.y + y;
    
        this.previous = this.current;
        this.current = this.x + this.grid_size * this.y;
    
        // Change color of the tile player stepped on
        let current_color = this.grid_colors[this.current];
        if (![this.five, this.six].includes(current_color)) {
            this.grid_colors[this.current] = "0";
        }
    
        if ([this.one, this.two, this.three, this.four, this.five, this.six].includes(current_color)) {
            this.addSteppedTileToContainer(current_color);
        }
    
        // re-initialize grid with updated colors
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four, this.five, this.six);  // Pass this.one to the Grid
        this.draw();
                // End game if current position is where 'tile-6' is located
                if ($(".grid-item").eq(this.current).hasClass("tile-background-5")) {
                    console.log('Trying to show Boiling...');
                    $(".boiling-message").removeClass('hidden');
        // Debugging log
                    // Add the 'hidden' class to hide these elements
                    $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").addClass('hidden'); // Directly show the boiling message without 'hidden' class
                    $(".boiling-message").addClass('show');
                
                    setTimeout(() => {
                        console.log('Hiding Boiling...'); // Debugging log
                        // Directly hide the "boiling..." message after the timeout
                        $(".boiling-message").removeClass('show');
                        $(".boiling-message").addClass('hidden');
        
                        // Remove the 'hidden' class to show these elements again
                        $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").removeClass('hidden');
                    }, 1000); // Display "Boiling..." for 3 seconds
                }

                if ($(".grid-item").eq(this.current).hasClass("tile-background-6"))  {
                    console.log('Trying to show Grinding...');
                    $(".grinding-message").removeClass('hidden');
        // Debugging log
                    // Add the 'hidden' class to hide these elements
                    $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").addClass('hidden'); // Directly show the boiling message without 'hidden' class
                    $(".grinding-message").addClass('show');
                
                    setTimeout(() => {
                        console.log('Hiding Grinding...'); // Debugging log
                        // Directly hide the "boiling..." message after the timeout
                        $(".grinding-message").removeClass('show');
                        $(".grinding-message").addClass('hidden');
        
                        // Remove the 'hidden' class to show these elements again
                        $(".your_turn, .instructions, #stepped-images-container, .grid-container, .tutorial_player").removeClass('hidden');
                    }, 1000); // Display "Boiling..." for 3 seconds
                }
                
    }

    addSteppedTileToContainer(currentColor) {
        const tile = $("<div/>", {
            "class": `tile-background-${currentColor} collected-tile`
        });
        $("#stepped-images-container").append(tile);

            
        // The AJAX call is updated here to use the correct content type
        // and send the data in JSON format.
        
    }
    
    
}


$(function () {
    // lazy load fonts
    $.ajax({
        url: "/static/css/fonts.css",
        beforeSend: x => {
            x.overrideMimeType("application/octet-stream")
        },
        success: () => {
            $("<link/>", {
                rel: "stylesheet",
                href: "/static/css/fonts.css"
            }).appendTo("head")
        }
    })

    // button animations
    $(document).on("mousedown touchstart", ".button", function () { $(this).addClass("click") })
    $(document).on("mouseup touchend", () => { $(".button").removeClass("click") })

    // empty contenteditable divs on focusout
    $(document).on("focusout", "div[contenteditable]", function () {
        var element = $(this)
        if (!element.text().trim().length) element.empty()
    })

    // div contenteditable to input automatically
    $(document).on("input change keyup", "div[contenteditable]", function () {
        var id = "input[name=" + $(this).attr("id") + "]"
        var v = $(this).text()
        if (!$(id).length) {
            $(this).parent().append(
                $("<input/>", { type: "hidden", name: $(this).attr("id"), value: v }))
        } else {
            $(id).val(v)
        }

        $(id).trigger("input")
    })
})

// When the player navigates to Introduction0.html
$(document).ready(function() {
    if (window.location.pathname.endsWith('/Introduction0')) {
        // Make an API call to set the intro timestamp
        $.post("/api/set_intro_timestamp");
    }
});

// When the player navigates to play.html
$(document).ready(function() {
    if (window.location.pathname.endsWith('/play')) {
        // Make an API call to set the play timestamp and calculate direction_time
        $.post("/api/set_play_timestamp");
    }
});

function saveGameState() {
    const gameState = {
        grid_colors: this.grid_colors,
        score: this.score,
        x: this.x,
        y: this.y,
        steps_remaining: this.steps_remaining,
        lastTile: this.lastTile
        // ... add any other game state variables you need
    };
    localStorage.setItem('gameState', JSON.stringify(gameState));
}

function loadGameState() {
    const savedState = localStorage.getItem('gameState');
    if (savedState) {
        const gameState = JSON.parse(savedState);
        this.grid_colors = gameState.grid_colors;
        this.score = gameState.score;
        this.x = gameState.x;
        this.y = gameState.y;
        this.steps_remaining = gameState.steps_remaining;
        this.lastTile = gameState.lastTile;
        // ... load other game state variables
        this.draw();  // or whatever function redraws your game board
    }
} 
