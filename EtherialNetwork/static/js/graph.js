function NetworkGraphGenerator(artist_name) {
// set the dimensions and margins of the graph
  const margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = window.innerWidth - margin.left - margin.right,
    height = window.innerHeight - margin.top - margin.bottom;
  
  // append the svg object to the body of the page
  const svg = d3.select("#my_dataviz")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            `translate(${margin.left}, ${margin.top})`);

  // node sizing


  function searchTracks(tracks_id_list, links) {
    var trackInfo = {
      "trackNames" : [],
      "trackIds" : []
    }
    
    for (let i = 0; i < tracks_id_list.length; i++) {
      const track_id = tracks_id_list[i];
      for (let j = 0; j < links.length; j++) {
        const link = links[j];
        if (link.track_id == track_id) {
          trackInfo.trackNames.push(link.name);
          trackInfo.trackIds.push(link.track_id);
          break;
        }
      }
    }
    console.log(trackInfo.trackNames);
    console.log(trackInfo.trackIds);
    
    return trackInfo;
  }


  function nodeInfoUI(node, tracklist) {

    var modal = document.querySelector(".modal")
    var modalTitle = document.querySelector(".modal-title")
    var modalImage = document.querySelector(".modal-img")
    var modalSubtitle = document.querySelector(".modal-subtitle")
    var modalTrackList = document.querySelector(".modal-right")
    var modalTrackPreview = document.querySelector(".modal-preview")

    modal.style.display = "block";

    modalTitle.textContent = node.name;
    modalImage.src = node.img_url;
    modalSubtitle.textContent = "Followers: " + Intl.NumberFormat().format(node.followers);
    modalTrackList.innerHTML = "";
    modalTrackPreview.src = "https://open.spotify.com/embed/track/" + tracklist.trackIds[0]


    var releaseHeader = document.createElement('div')
    var trackNameHeader = document.createElement('div')
    var popularityHeader = document.createElement('div')
    var durationHeader = document.createElement('div')
    
    releaseHeader.innerText = 'Release Date'
    trackNameHeader.innerText = 'Track Name'
    popularityHeader.innerText = 'Popularity'
    durationHeader.innerText = 'Duration'

    var headerBar = document.createElement('div')
    headerBar.classList.add('header-bar')
    headerBar.appendChild(releaseHeader)
    headerBar.appendChild(trackNameHeader)
    headerBar.appendChild(popularityHeader)
    headerBar.appendChild(durationHeader)
    modalTrackList.appendChild(headerBar)

    

    for(i = 0; i < tracklist.trackNames.length; i++) {
      var trackWrapper = document.createElement('div')
      trackWrapper.classList.add('track-wrapper')


      var track = document.createElement('div');
      track.classList.add('track_name')


      track.textContent =  (i+1)  + ". " + tracklist.trackNames[i]
      track.id = tracklist.trackIds[i]
     
      // Use a closure to capture the current value of tracklist.trackIds[i]
      track.onclick = (function(id) {
        return function() {
            changeSong(id);
        };
      })(tracklist.trackIds[i]);
      modalTrackList.appendChild(track)

    }

    //console.log(node)
    //document.querySelector("overlay").style.display = "block";
  }


  function nodeTrackList(track_list) {
    searchTracks()
  }


  function displayLinks(link) {
    console.log(link)

  }

  function fileNameEditor() {
    console.log("eeepy")
  }

  fetch('/playlist')
    .then(response => response.text())
    .then(data => {
      // Get the div element by its ID
      //console.log(data)
      // Set the innerHTML of the div to the JSON data
      //let pl_url = data
      //console.log(pl_url)
      
      d3.json(artist_name).then(function(data) {

        const sizeScale = d3.scaleLinear()
        .domain(d3.extent(data.nodes, d => d.tracklist.length))
        .range([32, 64]);
        const boundary = { x: 0, y: 0, width: width, height: height };
      
      
        // Initialize the links
        const link = svg
          .selectAll("line")
          .data(data.links)
          .join("line")
            .style("stroke", "#aaa")
          .on("click", function(d, i) {
            displayLinks(i)
          })
      
          
      
        // Initialize the nodes
        const node = svg
          .selectAll("image")
          .data(data.nodes)
          .join("image")
            .attr("xlink:href", (d) => d.img_url)
            .attr("width", d => sizeScale(d.tracklist.length) + 2)
            .attr("height", d => sizeScale(d.tracklist.length) + 2)
            .style("clip-path", "circle(50%)")
            .style("cursor", "pointer")
            .on("click", function(d, i) {
              trackInfo = searchTracks(i.tracklist, data.links)
              nodeInfoUI(i, trackInfo)
              
      
            })
            
        const label = svg
          .selectAll("text")
          .data(data.nodes)
          .enter()
          .append("text")
          .attr("textLength", function(d) {
            return Math.min(2*sizeScale(d.tracklist.length), this.getComputedTextLength());
          })
          .attr("lengthAdjust", "spacingAndGlyphs")
          .text((d) => d.name)
          .style("fill", "#fff")
          .style("font-size", "0.75rem")
          .style("text-anchor", "middle")
      
      
      
        // Let's list the force we wanna apply on the network
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink()
                  .id(function(d) { return d.artist_id; })
                  .links(data.links)
                  .distance(d => d.collab_count*2 + 90)
            )
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide().radius(d => sizeScale(d.tracklist.length) + 2).strength(1).iterations(1))
      
            
            .on("tick", ticked);
      
        function ticked() {
            
            link.attr("x1", function(d) { return d.source.x + sizeScale(d.source.tracklist.length)/2; })
            .attr("y1", function(d) { return d.source.y + sizeScale(d.source.tracklist.length)/2; })
            .attr("x2", function(d) { return d.target.x + sizeScale(d.target.tracklist.length)/2; })
            .attr("y2", function(d) { return d.target.y + sizeScale(d.target.tracklist.length)/2; });
      
      
            node.attr("transform", function(d) {
              d.x = Math.max(sizeScale(d.tracklist.length), Math.min(width - sizeScale(d.tracklist.length), d.x));
              d.y = Math.max(sizeScale(d.tracklist.length), Math.min(height - sizeScale(d.tracklist.length), d.y));
              return `translate(${d.x}, ${d.y})`;
            })
            .call(drag(simulation));
      
            label.attr("x", function(d) { return d.x + sizeScale(d.tracklist.length)/2; })
              .attr("y", function(d) { return d.y + sizeScale(d.tracklist.length)*1.25;})
              .attr("text-anchor", "middle");
            }
      
        function drag(simulation) {
          function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }
      
          function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
          }
      
          function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }
      
          return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
        }
      
      
        node.append("title").text((d) => d.name);
      
      });
    })
    .catch(error => {
      console.error(error);
    });



}

//  Generates onclick function for a button
function artistButton(artistName) {
  var button = document.getElementById(artistName).onclick = function() {
    graphDiv = document.querySelector('.graph')
    while (graphDiv.firstChild) {
      graphDiv.removeChild(graphDiv.lastChild);
    }
    NetworkGraphGenerator("/static/data/" + artistName + ".json")
  
  }
  return button
}

//  Generates the button on the website
function renderArtistButton(artistName, aName, imgUrl) {

  //  Create the button element
  var button = document.createElement('button')

  //  Set button type
  button.setAttribute('type', 'button')

  //  Set button class
  button.className = 'artist-btn'

  //  Set button id
  button.id = artistName

  //  Set overlay innertext
  //button.innerText = aName

  //  Set bg
  button.style.backgroundImage = `url(${imgUrl})`

  //  Create text element
  var aText = document.createElement('div');
  aText.classList.add('artist-text-overlay');
  aText.innerText = aName
  // Create the overlay element
  var overlay = document.createElement('div');
  overlay.classList.add('artist-btn-overlay'); // Add a class for styling

  // Append the overlay to the button
  button.appendChild(aText)
  button.appendChild(overlay);


  // Find the element with the specified class (replace 'playlists' with the actual class of your container)
  var playlistsContainer = document.querySelector('.playlists');

  // Append the button to the playlists container
  playlistsContainer.appendChild(button);


}

//  Generates all the buttons for the artists in the JSON file
function generateAllArtistButtons() {

  //  Read JSON
  fetch('static/data/playlist-information.json')
    .then((response) => response.json())
    .then((json) => {

      json['artists'].forEach(artist => {
        //  Generating buttons on the website
        renderArtistButton(artist.name, artist.aName, artist.imgUrl)


        //  Generating button onclick
        artistButton(artist.name)
      });

    }
      
      
      //  Generate buttons based on JSON data
      
      

    );

  
}


//  Music Controller
function changeSong(trackId) {
  
  console.log(trackId)
  // Use AJAX to send a request to your Flask server
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/changeSong?trackId=" + trackId, true);
  xhr.send();

  var track = document.getElementById(trackId)
  track.style.backgroundColor = '#4d4d4d'
}


generateAllArtistButtons()



