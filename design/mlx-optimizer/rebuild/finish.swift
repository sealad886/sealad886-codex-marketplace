// Mask Apple's export to the custom slate silhouette, then audit and make review proofs.
import AppKit
import Foundation
let root=CommandLine.arguments[1]
let names=["mlx-tile","mlx-m-hook","mlx-rails"]
func read(_ path:String)->CGImage {NSBitmapImageRep(data:try! Data(contentsOf:URL(fileURLWithPath:path)))!.cgImage!}
func ctx(_ width:Int,_ height:Int)->CGContext {CGContext(data:nil,width:width,height:height,bitsPerComponent:8,bytesPerRow:width*4,space:CGColorSpace(name:CGColorSpace.sRGB)!,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!}
func save(_ image:CGImage,_ name:String){try! NSBitmapImageRep(cgImage:image).representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:root+"/"+name+".png"))}
func resized(_ image:CGImage,_ size:Int)->CGImage{let c=ctx(size,size);c.interpolationQuality = .high;c.draw(image,in:CGRect(x:0,y:0,width:size,height:size));return c.makeImage()!}
func pixels(_ image:CGImage)->[UInt8]{let c=ctx(image.width,image.height);c.draw(image,in:CGRect(x:0,y:0,width:image.width,height:image.height));return Array(UnsafeBufferPointer(start:c.data!.assumingMemoryBound(to:UInt8.self),count:image.width*image.height*4))}
func audit(_ image:CGImage)->[String:Any]{let w=image.width,h=image.height,b=pixels(image);var zero=0,partial=0,opaque=0,edge=0;var visited=[Bool](repeating:false,count:w*h),components:[Int]=[]
 for i in 0..<w*h {let a=Int(b[i*4+3]);if a==0 {zero+=1}else if a==255 {opaque+=1}else{partial+=1};let x=i%w,y=i/w;if x==0 || x==w-1 || y==0 || y==h-1 {edge=max(edge,a)}}
 for start in 0..<w*h where b[start*4+3]>2 && !visited[start]{var queue=[start],head=0;visited[start]=true;while head<queue.count{let i=queue[head];head+=1;let x=i%w,y=i/w;for (dx,dy) in [(-1,0),(1,0),(0,-1),(0,1)]{let nx=x+dx,ny=y+dy;if nx>=0 && nx<w && ny>=0 && ny<h{let j=ny*w+nx;if !visited[j] && b[j*4+3]>2{visited[j]=true;queue.append(j)}}}};components.append(queue.count)}
 return ["width":w,"height":h,"mode":"RGBA8","zeroAlphaPixels":zero,"partialAlphaPixels":partial,"opaquePixels":opaque,"edgeMaxAlpha":edge,"cornerAlpha":[b[3],b[(w-1)*4+3],b[(h-1)*w*4+3],b[(w*h-1)*4+3]],"connectedComponentsAboveAlpha2":components.sorted(by:>)]}
let layers=names.map{read(root+"/"+$0+".png")}
let mask=pixels(resized(layers[0],1024))
var finished:[CGImage]=[]
for (input,output) in [("composer-raw","composer-preview"),("composer-dark-raw","composer-dark-preview")]{let image=read(root+"/"+input+".png"),b=pixels(image),c=ctx(1024,1024),p=c.data!.assumingMemoryBound(to:UInt8.self)
 for i in 0..<1024*1024{let a=Double(mask[i*4+3])/255;for j in 0..<4{p[i*4+j]=UInt8(Double(b[i*4+j])*a)};if mask[i*4+3]<255 {for j in 0..<3 {p[i*4+j]=mask[i*4+j]}}}
 let result=c.makeImage()!;save(result,output);finished.append(result)
}
for size in [32,64,128,256]{save(resized(finished[0],size),"composer-preview-\(size)")}
var report:[String:Any]=[:];for (i,name) in names.enumerated(){report[name]=audit(layers[i])};report["composer-preview"]=audit(finished[0]);report["composer-dark-preview"]=audit(finished[1]);try! JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys]).write(to:URL(fileURLWithPath:root+"/alpha-audit.json"))
let colors:[CGColor]=[CGColor(red:1,green:1,blue:1,alpha:1),CGColor(red:0,green:0,blue:0,alpha:1),CGColor(red:0.62,green:0,blue:0.85,alpha:1),CGColor(red:0,green:0.92,blue:0.2,alpha:1)]
let sheet=ctx(1280,1280)
for row in 0..<4 {for col in 0..<4 {let r=CGRect(x:col*320,y:(3-row)*320,width:320,height:320);sheet.setFillColor(colors[col]);sheet.fill(r);sheet.draw(row<3 ? layers[row]:finished[0],in:r)}};save(sheet.makeImage()!,"review-proof-sheet")
let small=ctx(800,280);small.setFillColor(CGColor(red:0.12,green:0.13,blue:0.15,alpha:1));small.fill(CGRect(x:0,y:0,width:800,height:280));var x=20;for size in [32,64,128,256]{small.draw(resized(finished[0],size),in:CGRect(x:x,y:12,width:size,height:size));x+=size+40};save(small.makeImage()!,"review-small-sizes")
print(String(data:try! JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys]),encoding:.utf8)!)
