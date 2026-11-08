import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public class PointDemo {
    static class Point {
        final int x, y;
        Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            return o instanceof Point p && p.x == x && p.y == y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x,y);
        }
    }

    public static void main(String[] args) {
        Point a = new Point(1,2);
        Point b = new Point(1,2);

        System.out.println("a.equal(b): " + a.equals(b));
        System.out.println("a.hashCode(): " + a.hashCode());
        System.out.println("b.hashCode(): " + b.hashCode());

        Map<Point, String> map = new HashMap<>();

        map.put(a, "khobar");
        System.out.println("get(a): " + map.get(a));
        System.out.println("get(b): " + map.get(b));
    }
}