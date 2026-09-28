// Deterministic, editable MLX icon artwork. Coordinates share a 1024-point canvas.
import AppKit
import CoreGraphics
import Foundation
let out = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "."
let resolution = 2048
func color(_ hex: UInt32, _ alpha: CGFloat = 1)->CGColor { CGColor(red:CGFloat((hex>>16)&255)/255,green:CGFloat((hex>>8)&255)/255,blue:CGFloat(hex&255)/255,alpha:alpha) }
func context(_ size:Int=resolution)->CGContext {let c=CGContext(data:nil,width:size,height:size,bitsPerComponent:8,bytesPerRow:size*4,space:CGColorSpace(name:CGColorSpace.sRGB)!,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!;c.scaleBy(x:CGFloat(size)/1024,y:CGFloat(size)/1024);c.translateBy(x:0,y:1024);c.scaleBy(x:1,y:-1);return c}
func save(_ image:CGImage,_ name:String) { let b=NSBitmapImageRep(cgImage:image);try! b.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:out+"/"+name+".png")) }
func strokeShape(_ p:CGPath,_ width:CGFloat)->CGPath {p.copy(strokingWithWidth:width,lineCap:.round,lineJoin:.round,miterLimit:10)}
func fill(_ c:CGContext,_ p:CGPath,_ col:CGColor){c.addPath(p);c.setFillColor(col);c.fillPath()}
func stroke(_ c:CGContext,_ p:CGPath,_ width:CGFloat,_ col:CGColor){c.addPath(p);c.setStrokeColor(col);c.setLineWidth(width);c.setLineCap(.round);c.setLineJoin(.round);c.strokePath()}
let tile=CGPath(roundedRect:CGRect(x:55,y:55,width:914,height:914),cornerWidth:196,cornerHeight:196,transform:nil)
// Single continuous M stroke: the right leg turns left into the hooked foot.
// No duplicate descending diagonal is hidden underneath the rail.
let m=CGMutablePath();m.move(to:CGPoint(x:239,y:664));m.addLine(to:CGPoint(x:239,y:235));m.addLine(to:CGPoint(x:485,y:449));m.addLine(to:CGPoint(x:746,y:235));m.addLine(to:CGPoint(x:746,y:622));m.addLine(to:CGPoint(x:546,y:819))
func input(_ y:CGFloat)->CGPath {let p=CGMutablePath();p.move(to:CGPoint(x:162,y:y));p.addLine(to:CGPoint(x:304,y:y));if y<545 {p.addCurve(to:CGPoint(x:512,y:545),control1:CGPoint(x:393,y:y),control2:CGPoint(x:410,y:545))} else if y>545 {p.addCurve(to:CGPoint(x:512,y:545),control1:CGPoint(x:393,y:y),control2:CGPoint(x:410,y:545))} else {p.addLine(to:CGPoint(x:512,y:545))};return p}
let rail=CGMutablePath();rail.move(to:CGPoint(x:512,y:545));rail.addLine(to:CGPoint(x:600,y:545));rail.addCurve(to:CGPoint(x:654,y:573),control1:CGPoint(x:625,y:545),control2:CGPoint(x:638,y:554));rail.addLine(to:CGPoint(x:847,y:802))
let paths=[input(415),input(545),input(675),rail]
let hues:[UInt32]=[0x29f5e0,0x27b6ff,0xffac37,0xd7f4ff]
func material(_ shape:CGPath,_ kind:String)->CGImage {
 let size=resolution,scale=Double(size)/1024
 let mask=context();fill(mask,shape,color(0xffffff));let im=mask.makeImage()!
 let bytes=Array(im.dataProvider!.data! as Data)
 let n=size*size
 var d=[Float](repeating:100000,count:n)
 for i in 0..<n {if bytes[i*4+3]<128 {d[i]=0}}
 let diagonal:Float=1.41421356
 for y in 1..<size {for x in 1..<size-1 {let i=y*size+x;d[i]=min(d[i],d[i-1]+1,d[i-size]+1,d[i-size-1]+diagonal,d[i-size+1]+diagonal)}}
 for y in stride(from:size-2,through:0,by:-1) {for x in stride(from:size-2,through:1,by:-1) {let i=y*size+x;d[i]=min(d[i],d[i+1]+1,d[i+size]+1,d[i+size+1]+diagonal,d[i+size-1]+diagonal)}}
 // Smooth the distance field before computing normals to avoid chamfer banding.
 for _ in 0..<2 {
  var blur=d
  for y in 2..<size-2 {for x in 2..<size-2 {let i=y*size+x;blur[i]=(d[i-2]+d[i-1]+d[i]+d[i+1]+d[i+2])/5}}
  d=blur
  for y in 2..<size-2 {for x in 2..<size-2 {let i=y*size+x;blur[i]=(d[i-size*2]+d[i-size]+d[i]+d[i+size]+d[i+size*2])/5}}
  d=blur
 }
 let result=CGContext(data:nil,width:size,height:size,bitsPerComponent:8,bytesPerRow:size*4,space:CGColorSpace(name:CGColorSpace.sRGB)!,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
 let out=result.data!.assumingMemoryBound(to:UInt8.self)
 func smooth(_ a:Double,_ b:Double,_ x:Double)->Double {let t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)}
 func rgb(_ hex:UInt32)->[Double]{[Double((hex>>16)&255)/255,Double((hex>>8)&255)/255,Double(hex&255)/255]}
 for y in 1..<size-1 {for x in 1..<size-1 {
  let i=y*size+x,k=i*4,alpha=Double(bytes[k+3])/255
  if alpha==0 {continue}
  let px=Double(x)/scale,py=Double(y)/scale,dist=Double(d[i])/scale
  var gx=Double(d[i+1]-d[i-1])/2,gy=Double(d[i+size]-d[i-size])/2
  let length=max(0.001,hypot(gx,gy));gx/=length;gy/=length
  let bevel=kind=="rail" ? 20.0 : (kind=="metal" ? 9.0:7.0)
  let edge=max(0,min(1,dist/bevel))
  let slope=kind=="rail" ? sqrt(max(0,1-pow(edge,1.0))) : pow(1-edge,0.7)
  let nx = -gx*slope,ny = -gy*slope,nz=sqrt(max(0,1-slope*slope))
  let diffuse=max(0,nx * -0.38+ny * -0.52+nz*0.765)
  let spec=pow(max(0,nx * -0.38+ny * -0.48+nz*0.79),35)
  let lower=pow(max(0,nx*0.52+ny*0.65+nz*0.55),55)
  let hash=sin(px*12.9898+py*78.233)*43758.5453
  let grain=(hash-floor(hash)-0.5)
  var col:[Double]
  if kind=="tile" {
   let sheen=exp(-pow((px+py*0.7-230)/520,2))*0.085
   let v=0.022+diffuse*0.029+sheen+grain*0.019
   col=[v*0.9,v,v*1.15]
   let rim=(spec*0.65+lower*0.30)*(1-smooth(2,8,dist))
   for j in 0..<3 {col[j]+=rim}
  } else if kind=="metal" {
   let band=0.10+0.22*exp(-pow((px+py*0.52-435)/135,2))+0.08*exp(-pow((px-py*0.15-775)/55,2))
   let brushed=sin(py*8.1+sin(px*0.07))*0.005+grain*0.013
   let v=band*(0.55+diffuse*0.65)+brushed
   col=[v*0.79,v*0.89,v*1.08]
   let rimLight=spec*0.95+lower*0.48
   let ridge=exp(-pow((dist-1.7)/0.8,2))*0.28
   let groove=1-0.65*exp(-pow((dist-4.3)/1.25,2))
   for j in 0..<3 {col[j]=(col[j]+rimLight+ridge)*groove}
   let blue=pow(max(0,nx*0.65+ny * -0.5+nz*0.53),30)*(1-smooth(5,10,dist))
   col[1]+=blue*0.3;col[2]+=blue*0.8
  } else {
   let mix=smooth(410,506,px)
   let top=rgb(0x03cfbc),middle=rgb(0x008ce8),bottom=rgb(0xff870b)
   let blue=smooth(435,535,py),orange=smooth(558,650,py)
   var hue=(0..<3).map { (top[$0]*(1-blue)+middle[$0]*blue)*(1-orange)+bottom[$0]*orange }
   let white=rgb(0xd9f6ff)
   for j in 0..<3 {hue[j]=hue[j]*(1-mix)+white[j]*mix}
   let core=pow(smooth(6,20,dist),1.25)
   let glass=0.14+0.49*core+0.10*diffuse
   col=hue.map{$0*glass}
   let reflection=spec*1.8+lower*1.15
   let fresnel=pow(1-nz,4)*0.38
   for j in 0..<3 {col[j]+=reflection+fresnel*white[j]}
   // Energy rises along the descending stroke, rather than plateauing after the merge.
   let progress=max(0,min(1,((px-654)*193+(py-573)*229)/(193*193+229*229)))
   let power=smooth(468,617,px)*pow(smooth(3,19-progress*8,dist),0.8)*(0.27+0.9*pow(progress,0.8))
   for j in 0..<3 {col[j]+=power*white[j]}
   let sparkle=grain>0.486 && dist>8 ? 0.38:0.0
   for j in 0..<3 {col[j]+=sparkle}
   // White-hot convergence stays within the union tube instead of a pasted orb.
   let energy=exp(-pow((px-478)/48,2)-pow((py-545)/24,2))*0.95
   for j in 0..<3 {col[j]+=energy}
  }
  for j in 0..<3 {out[k+j]=UInt8(max(0,min(255,pow(max(0,col[j]),0.83)*255))*alpha)};out[k+3]=UInt8(alpha*255)
 }}
 return result.makeImage()!
}
let newTile=material(tile,"tile")
let newM=material(strokeShape(m,106),"metal")
let union=CGMutablePath();for p in paths {union.addPath(strokeShape(p,40))}
struct DischargeRandom {
 var state:UInt64
 mutating func next()->Double {state=state&+0x9e3779b97f4a7c15;var z=state;z=(z^(z>>30))&*0xbf58476d1ce4e5b9;z=(z^(z>>27))&*0x94d049bb133111eb;return Double(z^(z>>31))/Double(UInt64.max)}
}
func flatten(_ path:CGPath)->[CGPoint] {
 var result:[CGPoint]=[],current=CGPoint.zero
 path.applyWithBlock {pointer in
  let e=pointer.pointee
  switch e.type {
  case .moveToPoint: current=e.points[0];result.append(current)
  case .addLineToPoint:
   let end=e.points[0],start=current,count=max(1,Int(hypot(end.x-start.x,end.y-start.y)/9))
   for i in 1...count {let t=CGFloat(i)/CGFloat(count);result.append(CGPoint(x:start.x+(end.x-start.x)*t,y:start.y+(end.y-start.y)*t))};current=end
  case .addCurveToPoint:
   let start=current,a=e.points[0],b=e.points[1],end=e.points[2]
   for i in 1...35 {let t=CGFloat(i)/35,u=1-t;result.append(CGPoint(x:u*u*u*start.x+3*u*u*t*a.x+3*u*t*t*b.x+t*t*t*end.x,y:u*u*u*start.y+3*u*u*t*a.y+3*u*t*t*b.y+t*t*t*end.y))};current=end
  default: break
  }
 }
 return result
}
func electrify(_ glass:CGImage)->CGImage {
 let c=context();c.saveGState();c.translateBy(x:0,y:1024);c.scaleBy(x:1,y:-1);c.draw(glass,in:CGRect(x:0,y:0,width:1024,height:1024));c.restoreGState()
 let seeds:[UInt64]=[0x736c617465,0x6d656173757265,0x616d626572,0x706f776572]
 for (index,path) in paths.enumerated() {
  let raw=flatten(path);var rng=DischargeRandom(state:seeds[index]);let powerful=index==3
  var samples=[raw[0]],distance:CGFloat=0,target=CGFloat(5+rng.next()*9)
  for i in 1..<raw.count {distance+=hypot(raw[i].x-raw[i-1].x,raw[i].y-raw[i-1].y);if distance>=target {samples.append(raw[i]);distance=0;target=CGFloat(5+rng.next()*9)}}
  samples.append(raw.last!)
  c.saveGState();c.addPath(strokeShape(path,29));c.clip()
  for strand in 0..<(powerful ? 3:2) {
   var points:[CGPoint]=[];var displacement:CGFloat=0
   for i in 0..<samples.count {
    let p=samples[i],previous=samples[max(0,i-1)],next=samples[min(samples.count-1,i+1)]
    let dx=next.x-previous.x,dy=next.y-previous.y,l=max(0.001,hypot(dx,dy))
    let taper=CGFloat(min(1,Double(min(i,samples.count-1-i))/3))
    displacement=displacement*0.48+(CGFloat(rng.next())-0.5)*(powerful ? 16:12)
    let offset=displacement*taper + CGFloat(strand-1)*(powerful ? 3:2)
    points.append(CGPoint(x:p.x-dy/l*offset,y:p.y+dx/l*offset))
   }
   let bolt=CGMutablePath();bolt.move(to:points[0]);for p in points.dropFirst(){bolt.addLine(to:p)}
   let col=color(hues[index],strand==0 ? 0.85:0.43)
   c.saveGState();c.setShadow(offset:.zero,blur:powerful ? 5:3,color:col);stroke(c,bolt,powerful ? 1.6:0.95,color(0xedffff,strand==0 ? 0.98:0.65));c.restoreGState()
   // Independent forks break away from each stream, never repeating one bitmap.
   for i in 5..<points.count-4 where rng.next()<0.19 {
    let fork=CGMutablePath();fork.move(to:points[i]);let side:CGFloat=rng.next()<0.5 ? -1:1
    fork.addLine(to:CGPoint(x:points[i+1].x+side*3,y:points[i+1].y+side*6))
    fork.addLine(to:CGPoint(x:points[i+2].x-side*2,y:points[i+2].y+side*10))
    stroke(c,fork,0.65,color(0xd4f9ff,0.55))
   }
  }
  c.restoreGState()
 }
 // Increasing corona and irregular rim discharges make the lower half visibly energized.
 let start=CGPoint(x:654,y:573),end=CGPoint(x:847,y:802)
 let dx=end.x-start.x,dy=end.y-start.y,length=hypot(dx,dy),nx = -dy/length,ny=dx/length
 var surge=DischargeRandom(state:0x7375726765746970)
 for strand in 0..<3 {
  var previous=start,t:CGFloat=0,wander:CGFloat=0
  while t<1 {
   t=min(1,t+0.014+CGFloat(surge.next())*0.035)
   let side:CGFloat=strand%2==0 ? 1:-1
   wander=wander*0.4+(CGFloat(surge.next())-0.5)*(4+8*t)
   let offset=side*(5+9*t)+wander
   let point=CGPoint(x:start.x+dx*t+nx*offset,y:start.y+dy*t+ny*offset)
   let segment=CGMutablePath();segment.move(to:previous);segment.addLine(to:point)
   let intensity=pow(t,0.7)
   c.saveGState();c.setShadow(offset:.zero,blur:3+11*intensity,color:color(0x76dcff,0.2+0.6*intensity))
   stroke(c,segment,0.5+1.2*intensity,color(strand<2 ? 0xf3ffff:0x9de7ff,0.12+0.74*intensity));c.restoreGState()
   previous=point
  }
 }
 // The terminal core is the hottest part, contained by the rounded tube tip.
 c.saveGState();c.addPath(strokeShape(rail,36));c.clip()
 let terminal=CGMutablePath();terminal.move(to:CGPoint(x:794,y:739));terminal.addLine(to:end)
 c.setShadow(offset:.zero,blur:12,color:color(0xb8f0ff,0.95));stroke(c,terminal,9,color(0xffffff,0.9));c.restoreGState()
 return c.makeImage()!
}

let newRail=electrify(material(union,"rail"))
save(newTile,"mlx-tile");save(newM,"mlx-m-hook");save(newRail,"mlx-rails")
func finalComposite(_ size:Int,_ bg:CGColor?=nil)->CGImage {let c=context(size);if let bg=bg {c.setFillColor(bg);c.fill(CGRect(x:0,y:0,width:1024,height:1024))};c.saveGState();c.translateBy(x:0,y:1024);c.scaleBy(x:1,y:-1);c.draw(newTile,in:CGRect(x:0,y:0,width:1024,height:1024));c.saveGState();c.setShadow(offset:CGSize(width:0,height:-7),blur:12,color:color(0,0.7));c.draw(newM,in:CGRect(x:0,y:0,width:1024,height:1024));c.restoreGState();c.saveGState();c.setShadow(offset:CGSize(width:0,height:-7),blur:7,color:color(0,0.7));c.draw(newRail,in:CGRect(x:0,y:0,width:1024,height:1024));c.restoreGState();c.restoreGState();return c.makeImage()!}
for size in [32,64,128,256,1024,2048]{save(finalComposite(size),"composite-\(size)")}
for (name,col) in [("white",color(0xffffff)),("black",color(0)),("purple",color(0x9f00dc)),("green",color(0x00ed38))]{save(finalComposite(1024,col),"proof-"+name)}
print("Rendered dimensional material pass from shared geometry.")
