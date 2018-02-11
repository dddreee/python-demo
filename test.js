function getRandomLines(){
    var lines = [];
    for(var i = 0 ; i < 10 ; i++){
        var x = Math.round(Math.random()*100)
        var y = Math.round(Math.random() * (100 - x)) + x
        lines.push(
            {
                x: x,
                y: y
            }
        )
    }
    return lines

}
var lines = getRandomLines();
var time = 0;
function computeLineLength(lines){
    var mergedLines = [];
    for(var l in lines){
        var line = lines[l];
        if(!mergedLines.length){
            mergedLines.push({
                x: line.x,
                y: line.y
            });
        }else{
            for(var j in mergedLines){

                var line2 = mergedLines[j];
    
                if(line.x < line2.x && line.y < line2.y && line.y > line2.x){
                    line2.x = line.x;
                    
                }else if(line.x < line2.x && line.y > line2.y){
                    line2.x = line.x;
                    line2.y = line.y;
                   
    
                }else if(line.x > line2.x && line.y < line2.y){
                    
                }else if(line.y < line2.x || line.x > line2.y){
                    mergedLines.push({
                        x: line.x,
                        y: line.y
                    });
                    // console.log(4)
                }
            }
        }
    }

    if(lines.length === mergedLines.length){
        var len = 0
        for(var n in lines){
            len += (lines[n].y - lines[n].x)
        }
        return len;
    }else{
        var ls = mergedLines.slice(0);
        return computeLineLength(ls)

        
    }

    
}

var ln = computeLineLength(lines);
console.log(ln)