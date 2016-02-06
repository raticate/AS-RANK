<?php
 ini_set('memory_limit', '512M');
  //Txt in to an array
  $fileOpen = fopen('nodes.txt','r');
  if (!$fileOpen){
    echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
  }

  $index = 0; // contador de líneas
  while (!feof($fileOpen)) { // loop hasta que se llegue al final del archivo

    $index++;
    $line = fgets($fileOpen);   
    $nodos[$index] = explode("|",$line); // guardamos toda la línea en $line como un string
    $fileOpen++; // necesitamos llevar el puntero del archivo a la siguiente línea
  }

  $fileOpen = fopen('results.txt', 'r');
  if (!$fileOpen) {
    echo 'ERROR: No ha sido posible abrir el archivo. Revisa su nombre y sus permisos.'; exit;
  }

  $index = 0;
  while (!feof($fileOpen)) {
    $index++;
    $line = fgets($fileOpen); 
    $enlaces[$index] = explode("|",$line);
    $fileOpen++;
  }

  $file = fopen("asMap.json", "w");
  fwrite($file,'{"edges":[');
  for ($i = 1; $i < count($enlaces); $i++){
    fwrite($file, '{"source":"'.trim($enlaces[$i][0]).'",');
    fwrite($file, '"target":"'.trim($enlaces[$i][1]).'",');
    if(strcmp(trim($enlaces[$i][2]),'-1') == 0){fwrite($file, '"color":"rgba(255,0,0,0.075)","type":"curvedArrow",');}
    if(strcmp(trim($enlaces[$i][2]),'0') == 0){fwrite($file, '"color":"rgba(0,204,0,0.075)","type":"curvedArrow",');}
    if(strcmp(trim($enlaces[$i][2]),'2') == 0){fwrite($file, '"color":"rgba(0,0,225,0.075)","type":"curvedArrow",');}
    //fwrite($file, '"type":"curvedArrow",');
 	if(strcmp(trim($enlaces[$i][2]),'-1') == 0){fwrite($file, '"size":10,');}
    if(strcmp(trim($enlaces[$i][2]),'0') == 0){fwrite($file, '"size":10,');}
    if(strcmp(trim($enlaces[$i][2]),'2') == 0){fwrite($file, '"size":10,');}
	if($i != count($enlaces)-1){    
		fwrite($file, '"id":"'.$i.'"},');
	}else{
		fwrite($file, '"id":"'.$i.'"}');
	}
  }
 fwrite($file,'],"nodes":[');
  for ($i = 1; $i < count($nodos); $i++){
    fwrite($file, '{"id":"'.trim($nodos[$i][0]).'",');
    fwrite($file, '"label":"AS'.trim($nodos[$i][0]).'",');
    $rad = 3;
    if(intval(trim($nodos[$i][2]))>80){

		$radius = $rad;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}

	}else if(intval(trim($nodos[$i][2]))>60){
		
		$radius = $rad*2;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}

	}else if(intval(trim($nodos[$i][2]))>40){

		$radius = $rad*3;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}	

	}else if(intval(trim($nodos[$i][2]))>20){
		
		$radius = $rad*4;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}

	}else if(intval(trim($nodos[$i][2]))>10){
		
		$radius = $rad*5;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}

	}else{

		$radius = $rad*6;
		$x = rand(-$radius*1000,$radius*1000)/1000;
		fwrite($file, '"x":"'.$x.'",');
		$raiz = pow($radius,2)-pow($x,2);
		$y = sqrt($raiz);
		if(rand(0,1)>0.5){
			fwrite($file, '"y":"'.$y.'",');
		}else{
			fwrite($file,'"y":"'.-$y.'",');
		}
	
	}
    fwrite($file, '"size":'.trim($nodos[$i][2]).',');
    if($i != count($nodos)-1){
	    if(strcmp(trim($nodos[$i][1]),'ripencc') == 0){fwrite($file, '"color":"#4285F4","borderColor": "black","borderWidth": 3},');}
	    if(strcmp(trim($nodos[$i][1]),'afrinic') == 0){fwrite($file, '"color":"#EA4335","borderColor": "black","borderWidth": 3},');}
	    if(strcmp(trim($nodos[$i][1]),'arin') == 0){fwrite($file, '"color":"#FBBC05","borderColor": "black","borderWidth": 3},');}
	    if(strcmp(trim($nodos[$i][1]),'apnic') == 0){fwrite($file, '"color":"#34A853","borderColor": "black","borderWidth": 3},');}
	    if(strcmp(trim($nodos[$i][1]),'lacnic') == 0){fwrite($file, '"color":"#804000","borderColor": "black","borderWidth": 3},');}
    }else{
		if(strcmp(trim($nodos[$i][1]),'ripencc') == 0){fwrite($file, '"color":"#4285F4","borderColor": "#000","borderWidth": 3}');}
	    if(strcmp(trim($nodos[$i][1]),'afrinic') == 0){fwrite($file, '"color":"#EA4335","borderColor": "#000","borderWidth": 3}');}
	    if(strcmp(trim($nodos[$i][1]),'arin') == 0){fwrite($file, '"color":"#FBBC05","borderColor": "#000","borderWidth": 3}');}
	    if(strcmp(trim($nodos[$i][1]),'apnic') == 0){fwrite($file, '"color":"#34A853","borderColor": "#000","borderWidth": 3}');}
	    if(strcmp(trim($nodos[$i][1]),'lacnic') == 0){fwrite($file, '"color":"#804000","borderColor": "black","borderWidth": 3}');}
	}
  }
 fwrite($file,']}');
?>
