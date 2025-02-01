import { Button } from "@/components/ui/button"
import { Copy, ThumbsUp, ThumbsDown, Check } from 'lucide-react'
import { useState } from "react"
import { message } from "../../interfaces/interfaces"

interface MessageActionsProps {
  message: message
}

export function MessageActions({ message }: MessageActionsProps) {
  const [copied, setCopied] = useState(false)
  const [liked, setLiked] = useState(false)
  const [disliked, setDisliked] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleLike = () => {
    console.log("like")
    console.log(message.id)
    
    setLiked(!liked)
    setDisliked(false)
  }

  const handleDislike = () => {
    console.log("dislike")
    console.log(message.id)

    setDisliked(!disliked)
    setLiked(false)
  }

  return (
    <div className="flex items-center space-x-1">
      <Button variant="ghost" size="icon" onClick={handleCopy}>
        {copied ? (
            <Check className="text-black dark:text-white" size={16} />
        ) : (
            <Copy className="text-gray-500" size={16} />
        )}
      </Button>
      <Button variant="ghost" size="icon" onClick={handleLike}>
        <ThumbsUp className={liked ? "text-black dark:text-white" : "text-gray-500"} size={16} />
      </Button>
      <Button variant="ghost" size="icon" onClick={handleDislike}>
        <ThumbsDown className={disliked ? "text-black dark:text-white" : "text-gray-500"} size={16} />
      </Button>
    </div>
  )
}