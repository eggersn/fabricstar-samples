import scala.collection.{Map, _}

object HelloWorld extends App {
  var test:Map[String,Long] = Map()
  test += ("mychannel" -> 0)
  println(test("mychannel"))
  test -= "mychannel"
  test += ("mychannel" -> 1)
  println(test("mychannel"))
}