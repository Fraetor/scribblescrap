"use-client"

import dynamic from 'next/dynamic';
import React, { useRef, useEffect } from 'react'

const Canvas = function ({width, height, conf}) {
    if (typeof(window) === "undefined"){
        return (
        <div suppressHydrationWarning>
            <canvas className="w-full" ref={null} width={width} height={height} />
        </div>
        )
    }
    let scrap_img = new window.Image()
    scrap_img.src = conf.scrap_img_url

    let arm_img = new window.Image()
    arm_img.src = conf.arm_img_url

    let eye_img = new window.Image()
    eye_img.src = conf.eye_img_url

    let leg_img = new window.Image()
    leg_img.src = conf.leg_img_url

    let deco_img = new window.Image()

    if (typeof(conf.deco) !== "undefined"){
        deco_img.src = conf.deco
    }

    let accent_img = new window.Image()

    if (typeof(conf.accent) !== "undefined"){
        accent_img.src = conf.accent
    }


    let sway = 0
    let arm_sway = 0
    let leg_sway = 0
    let speed = 1+(0.25-Math.random()*0.5)

    let t = Math.random()*100

    const canvasRef = useRef(null)

    function update() {
        t += 0.016*speed
        sway = Math.sin(t * conf.sway_speed) * conf.sway_dist
        arm_sway = Math.sin(t * conf.arm_sway_speed) * conf.arm_sway_dist
        leg_sway = Math.sin(t * conf.leg_sway_speed) * conf.leg_sway_dist
    }

    const draw = (ctx) => {
        update()

        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

        ctx.save()
        ctx.translate(width / 2, height / 2)
        ctx.rotate(sway)
        ctx.scale(0.7, 0.7)

        for (var arm of conf.arms) {
            drawImage(
                ctx,
                arm_img,
                arm.ox, arm.oy,
                arm.rot + arm_sway,
                arm_img.width, arm_img.height,
                arm.rx, arm.ry)
        }

        for (var leg of conf.legs) {
            drawImage(
                ctx,
                leg_img,
                leg.ox, leg.oy,
                leg.rot + leg_sway,
                leg_img.width, leg_img.height,
                leg.rx, leg.ry)
        }


        drawImage(
            ctx,
            scrap_img,
            0, 0,
            0,
            512, 512)

        if (typeof(conf.deco) !== "undefined" ) {
            drawImage(
                ctx,
                deco_img,
                0,-280,
                0,
                deco_img.width,deco_img.height,
            )
        }
        
        if (typeof(conf.accent) !== "undefined" ) {
            drawImage(
                ctx,
                accent_img,
                80,-180,
                0,
                accent_img.width/4,accent_img.height/4,
            )
        }


        for (var eye of conf.eyes) {
            ctx.save()
            ctx.rotate(sway * 0.005 * eye.x)

            drawImage(
                ctx,
                eye_img,
                eye.x, eye.y,
                0, 80, 80)

            ctx.restore()
        }

        ctx.restore()
    }

    useEffect(() => {
        const canvas = canvasRef.current
        const context = canvas.getContext('2d')
        let frameCount = 0
        let animationFrameId

        //Our draw came here
        const render = () => {
            frameCount++
            draw(context, frameCount)
            animationFrameId = window.requestAnimationFrame(render)
        }
        render()

        return () => {
            window.cancelAnimationFrame(animationFrameId)
        }
    }, [draw])

    function drawImage(ctx, img, x, y, r=0, w=img.width, h=img.height, ox=w/2, oy=h/2) {
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(r)
        ctx.drawImage(img, -ox, -oy, w, h)
        ctx.restore()
    }

    return (
        <div suppressHydrationWarning>
            <canvas className="w-full" ref={canvasRef} width={width} height={height} />
        </div>
    )
}

export default Canvas
