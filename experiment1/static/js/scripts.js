// function sleep(ms) {
//     return new Promise(resolve => setTimeout(resolve, ms))
// }

// class Grid {
//     constructor(colors, element, one, two, three, four) {
//         this.grid = $("<div/>", { "class": "grid" })
//         this.gridItems = []
//         this.one = one
//         this.two = two
//         this.three = three
//         this.four = four

//         // Extract game level from the URL
//         this.gameLevel = parseInt(window.location.pathname.split('/')[1]);
        
//         // empty container
//         element.empty()

//         // fill colors to grid
//         for (let i = 0; i < colors.length; i++) {
//             let item = $("<div/>", { "class": "grid-item" })
//             item.addClass(`tile-background-${colors[i]}`)
//             this.gridItems = [...this.gridItems, item]
//             $(this.grid).append(item)
//         }

//         $(this.grid).appendTo(element)
//         this.adjustSize()
//     }

//     //makes a square
//     adjustSize() {
//         this.grid.width(this.grid.height())
//     }
// }



// //represents main game state and logic
// class Game {
//     constructor(steps, grid_element) {
//         this.steps = steps

//         this.x = 0
//         this.y = 0
//         this.current = 0
//         this.previous = null
//         this.active = true
//         this.score = 0
//         this.grid_element = grid_element;
//         this.lastTile = null;
//         this.tabSwitchCount = 0;


//         // get grid colors
//         $.getJSON("/api/board/create", data => {this.board_id = data.board.id
//             this.grid_colors = data.board.board
//             this.current = data.board.current_pos

//             this.grid_size = parseInt(Math.sqrt(this.grid_colors.length))

//             this.x = this.current % this.grid_size
//             this.y = (this.current - this.x) / this.grid_size

//             // update previous state
//             this.steps_remaining = data.board.moves_remaining
//             this.score = data.board.current_score

//             // get colors, sets this.x
//             this.zero = data.board.colors.colors[0]
//             this.one = data.board.colors.colors[1]
//             this.two = data.board.colors.colors[2]
//             this.three = data.board.colors.colors[3]
//             this.four = data.board.colors.colors[4]
//             console.log("created board")
//             this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four); // Pass this.one to the Grid
//             this.draw()

//         })

//         this.start_time = null

//         // add event handlers
//         this.addEventHandlers()
//         this.addTabVisibilityHandler();

    
//     }


//     scoreMove() {
//         let current_color = this.grid_colors[this.current];
//         if (current_color == "#B0BEC5") {
//             this.lastTile = current_color;
//             return; // No points are scored
//         } 
//         if (current_color == this.one) {
//             this.score += 1;
//             this.lastTile = current_color;
//         } else if (current_color == this.two) {
//             this.score -= 1;
//             this.lastTile = current_color;
//         } else if (current_color == this.three) {
//             if (this.lastTile == this.one) {
//                 this.score += 0; // Add the additional +2 points if the last tile was this.one
//             }
//             this.score += 1; 
//             this.lastTile = current_color;
//         } else if (current_color == this.four) {
//             this.score -= 1;
//             this.lastTile = current_color;
//         }
//     }
    

//     draw() {
//         $(".grid-item.active").removeClass("active")
//         $(".grid-item").eq(this.y * this.grid_size + this.x).addClass("active")

//         // update remaining steps display
//         $(".steps_left_data").html(this.steps_remaining)

//         // adjust size of grid
//         this.grid.adjustSize()
//     }

//     move(x, y) {
//         if (!this.active || this.steps_remaining <= 0) {
//             return;
//         }
    
//         // move by x, y; check if move is valid, adjust steps remaining
//         let future_x = this.x + x;
//         let future_y = this.y + y;
    
//         if (future_x < 0 || future_y < 0 || future_x >= this.grid_size || future_y >= this.grid_size) {
//             // invalid move
//             return;
//         }
    
//         // calculate index position
//         this.x = future_x;
//         this.y = future_y;
    
//         this.previous = this.current;
//         this.current = this.x + this.grid_size * this.y;
    
//         if (!this.start_time) {
//             this.start_time = Date.now();
//         }
    
//         this.scoreMove();
    
//         // Change color of the tile player stepped on
//         let current_color = this.grid_colors[this.current];
//         if (current_color == this.three) {
//             this.grid_colors[this.current] = "#B0BEC5";
//         } else if (current_color == this.one) {
//             this.grid_colors[this.current] = "#B0BEC5";
//         } else if (current_color == this.two) {
//             this.grid_colors[this.current] = "#B0BEC5";
//         } else if (current_color == this.four) {
//             this.grid_colors[this.current] = "#B0BEC5";
//         }

//         if ([this.one, this.two, this.three, this.four].includes(current_color)) {
//             this.addSteppedTileToContainer(current_color);
//         }


    
//         // save move to database
//         $.post("/api/move/create", {
//             move_x: x,
//             move_y: y,
//             total_score: this.score
//         }).done(data => {
//             this.steps_remaining -= 1;
//             if (this.steps_remaining <= 0) {
//                 this.end();
//             }
//             // Re-draw the grid with updated colors
//             this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);
//             this.draw();
//         }).fail(err => {
//             console.error(err);
//         });
//     }

//     end() {
//         this.active = false
//         let total_time = Math.round((Date.now() - this.start_time) / 1000)
//         $.post("/api/move/end", {
//             total_time: total_time,
//             total_score: this.score
//         }).done(data => {
//             $(".main").addClass("loading")
//             setTimeout(() => {
//                 // location.href = "/rules"
//                 // location.href = "/0/rules"
//                 location.href = `/${this.gameLevel}/rules`;
//             }, 5000)
//         })

//         this.grid.grid.animate({ opacity: 0.5 }, "slow")
//     }

//     //sets movements based on key code
//     addEventHandlers() {
//         $(document).on("keydown", function (e) {
//             if (e.keyCode == 37) {
//             // go left
//                 this.move(-1, 0)
//             } else if (e.keyCode == 38) {
//             // go up
//                 this.move(0, -1)
//             } else if (e.keyCode == 39) {
//             // go right
//                 this.move(1, 0)
//             } else if (e.keyCode == 40) {
//             // go down
//                 this.move(0, 1) 
//             } else if (e.keyCode == 32) {
//             // end
//                 this.end()
//             }

//         }.bind(this))
//     }

//     addTabVisibilityHandler() {
//         document.addEventListener('visibilitychange', () => {
//             if (document.hidden) {
//                 this.tabSwitchCount++;
//                 console.log(`Tab was switched ${this.tabSwitchCount} times.`);
                
//                 // Make an AJAX call to record the tab switch on the server
//                 $.post("/api/player/tabswitch", function(data) {
//                     // Handle response if necessary
//                     if (!data.success) {
//                         console.error("Failed to record tab switch.");
//                     }
//                 });
//             }
//         });
//     }


//     addSteppedTileToContainer(currentColor) {
//         const tile = $("<div/>", {
//             "class": `tile-background-${currentColor} collected-tile`
//         });
//         $("#stepped-images-container").append(tile);
//     }
    


// }

// class Tutorial {
//     constructor (grid_element, boards, colors, callback = null, time_between_moves = 1500, time_between_games = 5000) {
//         this.game = 0
//         this.x = 0
//         this.y = 0
//         this.current = 0
//         this.grid_element = grid_element
//         this.boards = boards
//         this.colors = colors
//         this.time_between_moves = time_between_moves
//         this.time_between_games = time_between_games
//         this.callback = callback
//         this.loadGame()
//     }

//     clearSteppedImageContainer() {
//         $("#stepped-images-container").html('<strong>Items eaten:</strong>');
//     }

//     loadGame() {
//         this.clearSteppedImageContainer();
//         var tut = this.boards[this.game]
//         if (!tut) {
//             this.callback()
//             return
//         }
    
//         // get colors
//         this.zero = this.colors[0]
//         this.one = this.colors[1]
//         this.two = this.colors[2]
//         this.three = this.colors[3]
//         this.four = this.colors[4]
    
//         // fill grid with colors of current player
//         this.grid_colors = tut.board.board_idx.map(c => this.colors[c])
//         this.grid_size = parseInt(Math.sqrt(this.grid_colors.length))
//         this.current = tut.board.initial_pos
//         this.x = this.current % this.grid_size
//         this.y = (this.current - this.x) / this.grid_size
    
//         // init grid
//         this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);  // Pass this.one to the Grid
//         this.draw()
    
//         // display player number
//         $(".tutorial_player").show()
//         $(".tutorial_player_data").text(this.game + 1)
    
//         // execute moves
//         this.playGame(tut.moves)
//     }

//     async playGame(moves) {
//         // go through all moves
//         for (let key = 0; key < moves.length; key++) {
//             await sleep(this.time_between_moves)
//             let v = moves[key]
//             this.move(v.move_x, v.move_y)
//         }

//         // end game
//         await sleep(this.time_between_moves)
//         this.grid.grid.addClass("loading")
//         await sleep(this.time_between_games)

//         // start next game
//         this.clearSteppedImageContainer();
//         this.game += 1
//         if (this.game >= this.boards.length) {
//             this.clearSteppedImageContainer();
//             // showed all games
//             if (this.callback) {
//                 this.callback()
//             } else {
//                 alert("showed all games")
//             }
//         } else {
//             this.grid.grid.removeClass("loading")
//             this.loadGame()
//         }
//     }

//     draw() {
//         $(".grid-item.active").removeClass("active")
//         $(".grid-item").eq(this.y * this.grid_size + this.x).addClass("active")
//         this.grid.adjustSize()
//     }


//     move(x, y) {
//         // calculate index position
//         this.x = this.x + x;
//         this.y = this.y + y;
    
//         this.previous = this.current;
//         this.current = this.x + this.grid_size * this.y;
    
//         // Change color of the tile player stepped on
//         let current_color = this.grid_colors[this.current];
//         this.grid_colors[this.current] = "0";
    
//         if ([this.one, this.two, this.three, this.four].includes(current_color)) {
//             this.addSteppedTileToContainer(current_color);
//         }
    
//         // re-initialize grid with updated colors
//         this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);  // Pass this.one to the Grid
//         this.draw();
//     }

//     addSteppedTileToContainer(currentColor) {
//         const tile = $("<div/>", {
//             "class": `tile-background-${currentColor} collected-tile`
//         });
//         $("#stepped-images-container").append(tile);
//     }
    
    
// }


// $(function () {
//     // lazy load fonts
//     $.ajax({
//         url: "/static/css/fonts.css",
//         beforeSend: x => {
//             x.overrideMimeType("application/octet-stream")
//         },
//         success: () => {
//             $("<link/>", {
//                 rel: "stylesheet",
//                 href: "/static/css/fonts.css"
//             }).appendTo("head")
//         }
//     })

//     // button animations
//     $(document).on("mousedown touchstart", ".button", function () { $(this).addClass("click") })
//     $(document).on("mouseup touchend", () => { $(".button").removeClass("click") })

//     // empty contenteditable divs on focusout
//     $(document).on("focusout", "div[contenteditable]", function () {
//         var element = $(this)
//         if (!element.text().trim().length) element.empty()
//     })

//     // div contenteditable to input automatically
//     $(document).on("input change keyup", "div[contenteditable]", function () {
//         var id = "input[name=" + $(this).attr("id") + "]"
//         var v = $(this).text()
//         if (!$(id).length) {
//             $(this).parent().append(
//                 $("<input/>", { type: "hidden", name: $(this).attr("id"), value: v }))
//         } else {
//             $(id).val(v)
//         }

//         $(id).trigger("input")
//     })
// })





// // When the player navigates to Introduction0.html
// $(document).ready(function() {
//     if (window.location.pathname.endsWith('/Introduction0')) {
//         // Make an API call to set the intro timestamp
//         $.post("/api/set_intro_timestamp");
//     }
// });

// // When the player navigates to play.html
// $(document).ready(function() {
//     if (window.location.pathname.endsWith('/play')) {
//         // Make an API call to set the play timestamp and calculate direction_time
//         $.post("/api/set_play_timestamp");
//     }
// });

// function saveGameState() {
//     const gameState = {
//         grid_colors: this.grid_colors,
//         score: this.score,
//         x: this.x,
//         y: this.y,
//         steps_remaining: this.steps_remaining,
//         lastTile: this.lastTile
//         // ... add any other game state variables you need
//     };
//     localStorage.setItem('gameState', JSON.stringify(gameState));
// }

// function loadGameState() {
//     const savedState = localStorage.getItem('gameState');
//     if (savedState) {
//         const gameState = JSON.parse(savedState);
//         this.grid_colors = gameState.grid_colors;
//         this.score = gameState.score;
//         this.x = gameState.x;
//         this.y = gameState.y;
//         this.steps_remaining = gameState.steps_remaining;
//         this.lastTile = gameState.lastTile;
//         // ... load other game state variables
//         this.draw();  // or whatever function redraws your game board
//     }
// }


// Add or modify existing custom CSS for the stepped images container
var customCSS = `
    #stepped-images-container {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: flex-start;
        gap: 5px; /* Adjust the gap between items as necessary */
        max-width: 500px; /* Set a max-width to prevent expansion */
        overflow-x: auto; /* Allow horizontal scrolling if needed */
    }
    .collected-tile {
        width: 40px; /* Adjust width based on your actual mushroom image width */
        height: 40px; /* Adjust height based on your actual mushroom image height */
        flex: 0 0 40px; /* Do not grow or shrink */
    }
    @media (max-width: 768px) {
        .your-turn-container {
            font-size: 14px; /* Adjust the font size for smaller screens */
        }
    }
`;
$("<style type='text/css'>").text(customCSS).appendTo("head");


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

class Grid {
    constructor(colors, element, one, two, three, four) {
        this.grid = $("<div/>", { "class": "grid" })
        this.gridItems = []
        this.one = one
        this.two = two
        this.three = three
        this.four = four

        // empty container
        element.empty()

        // fill colors to grid
        for (let i = 0; i < colors.length; i++) {
            let item = $("<div/>", { "class": "grid-item" })
            item.addClass(`tile-background-${colors[i]}`)
            this.gridItems = [...this.gridItems, item]
            $(this.grid).append(item)
        }

        $(this.grid).appendTo(element)
        this.adjustSize()
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
            this.zero = data.board.colors.colors[0]
            this.one = data.board.colors.colors[1]
            this.two = data.board.colors.colors[2]
            this.three = data.board.colors.colors[3]
            this.four = data.board.colors.colors[4]
            console.log("created board")
            this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four); // Pass this.one to the Grid
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
        if (current_color == "#B0BEC5") {
            this.lastTile = current_color;
            return; // No points are scored
        } 
        if (current_color == this.one) {
            this.score += 1;
            this.lastTile = current_color;
        } else if (current_color == this.two) {
            this.score -= 1;
            this.lastTile = current_color;
        } else if (current_color == this.three) {
            if (this.lastTile == this.one) {
                this.score += 0; // Add the additional +2 points if the last tile was this.one
            }
            this.score += 1; 
            this.lastTile = current_color;
        } else if (current_color == this.four) {
            this.score -= 1;
            this.lastTile = current_color;
        }

        console.log("current score", this.score)
    }
    

    draw() {
        $(".grid-item.active").removeClass("active")
        $(".grid-item").eq(this.y * this.grid_size + this.x).addClass("active")

        // update remaining steps display
        $(".steps_left_data").html(this.steps_remaining)

        // adjust size of grid
        this.grid.adjustSize()
    }

    move(x, y, record = true) {
        console.log("moving", x, y)
        if (!this.active || this.steps_remaining <= 0) {
            console.error("no longer active")
            return;
        }
    
        // move by x, y; check if move is valid, adjust steps remaining
        let future_x = this.x + x;
        let future_y = this.y + y;
    
        if (future_x < 0 || future_y < 0 || future_x >= this.grid_size || future_y >= this.grid_size) {
            // invalid move
            console.error("invalid move")
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
    
        // Change color of the tile player stepped on
        let current_color = this.grid_colors[this.current];
        if (current_color == this.three) {
            this.grid_colors[this.current] = "#B0BEC5";
        } else if (current_color == this.one) {
            this.grid_colors[this.current] = "#B0BEC5";
        } else if (current_color == this.two) {
            this.grid_colors[this.current] = "#B0BEC5";
        } else if (current_color == this.four) {
            this.grid_colors[this.current] = "#B0BEC5";
        }

        if ([this.one, this.two, this.three, this.four].includes(current_color)) {
            this.addSteppedTileToContainer(current_color);
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
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);
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
            if (e.keyCode == 37) {
            // go left
                this.move(-1, 0)
            } else if (e.keyCode == 38) {
            // go up
                this.move(0, -1)
            } else if (e.keyCode == 39) {
            // go righ
                this.move(1, 0)
            } else if (e.keyCode == 40) {
            // go down
                this.move(0, 1) 
            } else if (e.keyCode == 32) {
            // end
                this.end()
            }


        }.bind(this))
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


    addSteppedTileToContainer(currentColor) {
        const tile = $("<div/>", {
            "class": `tile-background-${currentColor} collected-tile`
        });
        $("#stepped-images-container").append(tile);
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
        $("#stepped-images-container").html('<strong>Items eaten:</strong>');
    }

    loadGame() {
        this.clearSteppedImageContainer();
        var tut = this.boards[this.game]
        if (!tut) {
            this.callback()
            return
        }
    
        // get colors
        this.zero = this.colors[0]
        this.one = this.colors[1]
        this.two = this.colors[2]
        this.three = this.colors[3]
        this.four = this.colors[4]
    
        // fill grid with colors of current player
        this.grid_colors = tut.board.board_idx.map(c => this.colors[c])
        this.grid_size = parseInt(Math.sqrt(this.grid_colors.length))
        this.current = tut.board.initial_pos
        this.x = this.current % this.grid_size
        this.y = (this.current - this.x) / this.grid_size
    
        // init grid
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);  // Pass this.one to the Grid
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
        this.grid_colors[this.current] = "0";
    
        if ([this.one, this.two, this.three, this.four].includes(current_color)) {
            this.addSteppedTileToContainer(current_color);
        }
    
        // re-initialize grid with updated colors
        this.grid = new Grid(this.grid_colors, this.grid_element, this.one, this.two, this.three, this.four);  // Pass this.one to the Grid
        this.draw();
    }

    addSteppedTileToContainer(currentColor) {
        const tile = $("<div/>", {
            "class": `tile-background-${currentColor} collected-tile`
        });
        $("#stepped-images-container").append(tile);
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
