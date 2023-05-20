var i=0;
var n=1;//counter

var cArray=["red","yellow","green","red","yellow","green","red","yellow","green","red","yellow","green"];
function trafficLight(){
    //let l=document.getElementsByClassName('light');//[3]
    let count =Math.floor(Math.random() * 13);
    let l=document.querySelectorAll(".light");
    console.log(l)

    

    for(var j=0;j<12;j++){
        l[j].style.background="black";
        l[j].innerHTML="";
    }

    l[i].style.background=cArray[i];
    if(i<12){  
        if(n<=count){ 
            l[i].innerHTML=n;
            if (cArray[i]=="yellow"){
                n = 14
            } 
            n++; 
            // i++; 
        }
        if(n>=count){ 
            i++;
            n=1; 
            // if(i==3){
            //     i=0;    
            // }   
        }
        if (i>=12 && n==count){
            i=0;
            n=1
        }
        
    }
    // for (let k=0; k<n; k++){
    //     l[0].innerHTML=k    
    // }

}


setInterval(trafficLight,1000);