export class CubeDraw {
    public redCount: number = 0;
    public greenCount: number = 0;
    public blueCount: number = 0;

    constructor(input: string) {
        const colorSegments = input.split(',');
        colorSegments.forEach((segment) => {
            const split = segment.trim().split(' ');
            const cubeCount = Number(split[0]);
            const colorName = split[1];

            this.setColor(colorName, cubeCount);
        });
    }

    private setColor(colorName: string, count: number): void {
        switch (colorName) {
            case 'red':
                this.redCount = count;
                break;
            case 'green':
                this.greenCount = count;
                break;
            case 'blue':
                this.blueCount = count;
                break;
        }
    }

    public toString(): string {
        return `Red: ${this.redCount}, Green: ${this.greenCount}, Blue: ${this.blueCount}`;
    }
}